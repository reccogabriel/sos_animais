from datetime import date

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


class AdocaoPrototipoForm(forms.Form):
    animal = forms.ChoiceField(
        label="Animal disponível",
        choices=[
            ("", "Selecione um animal"),
            ("rex", "Rex — cão, 3 anos, porte médio"),
            ("luna", "Luna — gata, 2 anos, porte pequeno"),
        ],
    )

    nome_adotante = forms.CharField(
        label="Nome do adotante",
        max_length=120,
    )

    telefone = forms.RegexField(
        label="Telefone do adotante",
        regex=r"^[0-9()+\s-]{10,20}$",
        max_length=20,
        error_messages={
            "invalid": (
                "Informe um telefone com DDD, usando "
                "números e, se necessário, espaços, "
                "parênteses ou hífen."
            ),
        },
    )

    data_adocao = forms.DateField(
        label="Data da adoção",
        initial=date.today,
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

        if self.is_bound:
            for nome in self.errors:
                if nome in self.fields:
                    campo = self.fields[nome]
                    campo.widget.attrs["aria-invalid"] = "true"
                    campo.widget.attrs["aria-describedby"] = (
                        f"erro_{nome}"
                    )

    def clean_data_adocao(self):
        valor = self.cleaned_data["data_adocao"]

        if valor > date.today():
            raise forms.ValidationError(
                "A data da adoção não pode ser futura."
            )

        return valor


def login_view(request):
    if request.user.is_authenticated:
        return redirect("menu")

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
            return redirect("menu")

        messages.error(
            request,
            "Usuário ou senha inválidos.",
        )

    return render(
        request,
        "core/login.html",
    )


@login_required(login_url="login")
def menu_view(request):
    return render(
        request,
        "core/menu.html",
    )


@login_required(login_url="login")
def registrar_adocao(request):
    form = AdocaoPrototipoForm(
        request.POST if request.method == "POST" else None
    )

    if request.method == "POST" and form.is_valid():
        dados = form.cleaned_data

        nomes_animais = dict(
            form.fields["animal"].choices
        )

        request.session["resultado_adocao_demo"] = {
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


@login_required(login_url="login")
def resultado_adocao(request):
    resultado = request.session.get(
        "resultado_adocao_demo"
    )

    if not resultado:
        return redirect("registrar_adocao")

    return render(
        request,
        "core/resultado_adocao.html",
        {"resultado": resultado},
    )