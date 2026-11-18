import re

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, resolve_url
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

CHAVE_SESSAO_RESULTADO = "resultado_adocao_demo"

# Apenas dígitos, espaços, parênteses, hífen e um "+" opcional no início.
CARACTERES_TELEFONE = re.compile(r"\+?[0-9()\s-]+")


# ---------------------------------------------------------------------------
# Endpoint de saúde — /health/
# ---------------------------------------------------------------------------
# Propósito: monitoramento externo (UptimeRobot) via HTTP(S) GET.
#
# O que verifica:
#   - Aplicação: sempre. O Django está em pé, o processo respondeu e a
#     configuração básica carregou sem erro.
#
# O que NÃO verifica deliberadamente:
#   - Banco de dados. Executar SELECT 1 a cada 5 minutos (intervalo mínimo
#     do UptimeRobot gratuito) pode impedir o scale-to-zero do Neon, que
#     suspende o compute após 5 minutos de inatividade. Manter o banco
#     artificialmente ativo consumiria cotas de CU-hora desnecessariamente.
#
# Verificação do banco (manual, quando necessário):
#   - Use o console SQL do Neon (dashboard > SQL Editor > SELECT 1).
#   - Ou execute localmente com DATABASE_URL apontando para o Neon:
#       python manage.py dbshell
#   - Não aponte o UptimeRobot para uma rota que faça SELECT 1.
#
# O que NÃO expõe: versão interna, stack trace, dados de usuários,
# SECRET_KEY, DATABASE_URL ou qualquer informação sensível.
def health_check(request):
    """
    Verifica apenas a aplicação (não toca no banco de dados).

    HTTP 200 → aplicação respondendo normalmente.
    Nunca retorna 5xx — se o Django chegou aqui, está em pé.
    """
    return JsonResponse({"status": "ok", "app": "ok"})


class AdocaoPrototipoForm(forms.Form):
    animal = forms.ChoiceField(
        label="Animal (fictício)",
        choices=[
            ("", "Selecione um animal fictício"),
            ("rex", "Rex, cão, 3 anos, porte médio (fictício)"),
            ("luna", "Luna, gata, 2 anos, porte pequeno (fictícia)"),
        ],
    )

    nome_adotante = forms.CharField(
        label="Nome do adotante",
        max_length=120,
    )

    telefone = forms.CharField(
        label="Telefone do adotante",
        max_length=20,
        help_text="Com DDD. Exemplo: (17) 99999-0000",
    )

    data_adocao = forms.DateField(
        label="Data da adoção",
        initial=timezone.localdate,
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"},
        ),
        input_formats=["%Y-%m-%d"],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for nome, campo in self.fields.items():
            campo.widget.attrs["class"] = (
                "form-select"
                if nome == "animal"
                else "form-control"
            )

            campo.error_messages["required"] = (
                "Preencha este campo para continuar."
            )

        self.fields["telefone"].widget.attrs.update(
            {
                "inputmode": "tel",
                "autocomplete": "tel",
            }
        )

        if self.is_bound:
            for nome in self.errors:
                if nome in self.fields:
                    campo = self.fields[nome]
                    campo.widget.attrs["aria-invalid"] = "true"
                    campo.widget.attrs["aria-describedby"] = (
                        f"erro_{nome}"
                    )

    def clean_telefone(self):
        valor = self.cleaned_data["telefone"].strip()

        if not CARACTERES_TELEFONE.fullmatch(valor):
            raise forms.ValidationError(
                "Use apenas números e, se necessário, espaços, "
                "parênteses, hífen ou o sinal + no início."
            )

        digitos = re.sub(r"\D", "", valor)

        if valor.startswith("+"):
            if not digitos.startswith("55"):
                raise forms.ValidationError(
                    "Informe um telefone do Brasil (+55) ou "
                    "digite o número sem o código do país."
                )
            digitos = digitos[2:]

        if len(digitos) not in (10, 11):
            raise forms.ValidationError(
                "Informe o DDD e o número: 10 dígitos para fixo "
                "ou 11 dígitos para celular."
            )

        return valor

    def clean_data_adocao(self):
        valor = self.cleaned_data["data_adocao"]

        if valor > timezone.localdate():
            raise forms.ValidationError(
                "A data da adoção não pode ser futura."
            )

        return valor


def _destino_seguro(request, destino):
    """Retorna o destino apenas se ele for um endereço deste site."""
    if destino and url_has_allowed_host_and_scheme(
        destino,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return destino
    return resolve_url(settings.LOGIN_REDIRECT_URL)


def login_view(request):
    proximo = request.POST.get("next") or request.GET.get("next", "")

    if request.user.is_authenticated:
        return redirect(_destino_seguro(request, proximo))

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect(_destino_seguro(request, proximo))

        messages.error(
            request,
            "Usuário ou senha inválidos.",
        )

    return render(
        request,
        "core/login.html",
        {"next": proximo},
    )


@require_POST
def logout_view(request):
    logout(request)
    messages.success(
        request,
        "Você saiu do sistema.",
    )
    return redirect(settings.LOGOUT_REDIRECT_URL)


@login_required
def menu_view(request):
    return render(
        request,
        "core/menu.html",
    )


@login_required
def registrar_adocao(request):
    form = AdocaoPrototipoForm(
        request.POST if request.method == "POST" else None
    )

    if request.method == "POST" and form.is_valid():
        dados = form.cleaned_data

        nomes_animais = dict(
            form.fields["animal"].choices
        )

        # Demonstração: os dados ficam na sessão apenas até a tela de
        # resultado ser exibida. Nada é gravado nas tabelas do sistema.
        request.session[CHAVE_SESSAO_RESULTADO] = {
            "animal": nomes_animais[dados["animal"]],
            "nome_adotante": dados["nome_adotante"],
            "telefone": dados["telefone"],
            "data_adocao": dados["data_adocao"].strftime(
                "%d/%m/%Y"
            ),
        }

        return redirect("resultado_adocao")

    return render(
        request,
        "core/adocao.html",
        {"form": form},
    )


@login_required
def resultado_adocao(request):
    # pop() lê e já remove nome e telefone do adotante da sessão.
    # Ao recarregar a página, a pessoa volta para o formulário.
    resultado = request.session.pop(
        CHAVE_SESSAO_RESULTADO,
        None,
    )

    if not resultado:
        return redirect("registrar_adocao")

    return render(
        request,
        "core/resultado_adocao.html",
        {"resultado": resultado},
    )
