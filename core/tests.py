from datetime import timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import connection
from django.test import SimpleTestCase, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from sos_animais.settings import env_bool, env_lista

from .models import Animal
from .views import CHAVE_SESSAO_RESULTADO, AdocaoPrototipoForm


class AnimalValidacaoTests(SimpleTestCase):
    def criar_animal(self, **alteracoes):
        dados = {
            "nome": "Rex",
            "especie": Animal.Especie.CAO,
        }
        dados.update(alteracoes)
        return Animal(**dados)

    def test_representacao_textual(self):
        animal = self.criar_animal()

        self.assertEqual(str(animal), "Rex — Cão")

    def test_valores_padrao(self):
        animal = self.criar_animal()

        self.assertEqual(animal.status, Animal.Status.ACOLHIDO)
        self.assertEqual(animal.porte, Animal.Porte.NAO_INFORMADO)
        self.assertEqual(animal.data_entrada, timezone.localdate())

    def test_nome_obrigatorio(self):
        animal = self.criar_animal(nome="")

        with self.assertRaises(ValidationError) as contexto:
            animal.clean_fields()

        self.assertIn("nome", contexto.exception.message_dict)

    def test_especie_invalida(self):
        animal = self.criar_animal(especie="invalida")

        with self.assertRaises(ValidationError) as contexto:
            animal.clean_fields()

        self.assertIn("especie", contexto.exception.message_dict)

    def test_status_invalido(self):
        animal = self.criar_animal(status="invalido")

        with self.assertRaises(ValidationError) as contexto:
            animal.clean_fields()

        self.assertIn("status", contexto.exception.message_dict)

    def test_observacoes_opcionais(self):
        animal = self.criar_animal(observacoes="")

        animal.clean_fields()

        self.assertEqual(animal.observacoes, "")


class AnimalPersistenciaTests(TestCase):
    def test_salva_e_recupera_animal(self):
        animal = Animal.objects.create(
            nome="Luna",
            especie=Animal.Especie.GATO,
            porte=Animal.Porte.PEQUENO,
            observacoes="Registro fictício para teste.",
        )

        recuperado = Animal.objects.get(pk=animal.pk)

        self.assertIsNotNone(recuperado.pk)
        self.assertEqual(recuperado.nome, "Luna")
        self.assertEqual(recuperado.especie, Animal.Especie.GATO)
        self.assertEqual(recuperado.porte, Animal.Porte.PEQUENO)
        self.assertEqual(recuperado.status, Animal.Status.ACOLHIDO)
        self.assertEqual(
            recuperado.observacoes,
            "Registro fictício para teste.",
        )
        self.assertIsNotNone(recuperado.criado_em)
        self.assertIsNotNone(recuperado.atualizado_em)

SENHA_TESTE = "SenhaDeTeste#2026"


def criar_usuario():
    return get_user_model().objects.create_user(
        username="equipe",
        password=SENHA_TESTE,
    )


class LoginTests(TestCase):
    def setUp(self):
        self.usuario = criar_usuario()
        self.url = reverse("login")

    def test_pagina_de_login_abre(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, "core/login.html")

    def test_senha_errada_nao_autentica(self):
        resposta = self.client.post(
            self.url,
            {"username": "equipe", "password": "errada"},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Usuário ou senha inválidos.")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_correto_vai_para_o_menu(self):
        resposta = self.client.post(
            self.url,
            {"username": "equipe", "password": SENHA_TESTE},
        )

        self.assertRedirects(resposta, reverse("menu"))
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            self.usuario.pk,
        )

    def test_login_respeita_next_interno(self):
        destino = reverse("registrar_adocao")

        resposta = self.client.post(
            f"{self.url}?next={destino}",
            {
                "username": "equipe",
                "password": SENHA_TESTE,
                "next": destino,
            },
        )

        self.assertRedirects(resposta, destino)

    def test_formulario_de_login_preserva_next(self):
        destino = reverse("registrar_adocao")

        resposta = self.client.get(f"{self.url}?next={destino}")

        self.assertContains(
            resposta,
            f'name="next" value="{destino}"',
        )

    def test_login_ignora_next_externo(self):
        resposta = self.client.post(
            self.url,
            {
                "username": "equipe",
                "password": SENHA_TESTE,
                "next": "https://site-malicioso.exemplo/",
            },
        )

        self.assertRedirects(resposta, reverse("menu"))

    def test_usuario_ja_logado_e_redirecionado(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(self.url)

        self.assertRedirects(resposta, reverse("menu"))


class AcessoProtegidoTests(TestCase):
    def setUp(self):
        self.usuario = criar_usuario()

    def test_paginas_exigem_login(self):
        for nome in ("menu", "registrar_adocao", "resultado_adocao"):
            with self.subTest(pagina=nome):
                url = reverse(nome)

                resposta = self.client.get(url)

                self.assertRedirects(
                    resposta,
                    f"{reverse('login')}?next={url}",
                )

    def test_menu_abre_para_usuario_logado(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse("menu"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, reverse("registrar_adocao"))
        self.assertContains(resposta, reverse("logout"))

    def test_menu_nao_tem_links_vazios(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse("menu"))

        self.assertNotContains(resposta, 'href="#"')

    def test_logout_por_post_encerra_a_sessao(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(reverse("logout"))

        self.assertRedirects(resposta, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertRedirects(
            self.client.get(reverse("menu")),
            f"{reverse('login')}?next={reverse('menu')}",
        )

    def test_logout_nao_aceita_get(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse("logout"))

        self.assertEqual(resposta.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)


def dados_adocao(**alteracoes):
    dados = {
        "animal": "rex",
        "nome_adotante": "Pessoa Fictícia",
        "telefone": "(17) 99999-0000",
        "data_adocao": timezone.localdate().isoformat(),
    }
    dados.update(alteracoes)
    return dados


class AdocaoFormularioTests(SimpleTestCase):
    def test_dados_validos(self):
        form = AdocaoPrototipoForm(data=dados_adocao())

        self.assertTrue(form.is_valid(), form.errors)

    def test_campos_obrigatorios(self):
        form = AdocaoPrototipoForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            set(form.errors),
            {"animal", "nome_adotante", "telefone", "data_adocao"},
        )

    def test_nome_so_com_espacos_e_recusado(self):
        form = AdocaoPrototipoForm(data=dados_adocao(nome_adotante="   "))

        self.assertIn("nome_adotante", form.errors)

    def test_animal_fora_da_lista_e_recusado(self):
        form = AdocaoPrototipoForm(data=dados_adocao(animal="bob"))

        self.assertIn("animal", form.errors)

    def test_data_futura_e_recusada(self):
        amanha = timezone.localdate() + timedelta(days=1)

        form = AdocaoPrototipoForm(
            data=dados_adocao(data_adocao=amanha.isoformat())
        )

        self.assertIn("data_adocao", form.errors)

    def test_telefones_validos(self):
        validos = [
            "(17) 99999-0000",
            "17999990000",
            "(17) 3281-0000",
            "1732810000",
            "+55 17 99999-0000",
            "+55 (17) 3281-0000",
        ]

        for telefone in validos:
            with self.subTest(telefone=telefone):
                form = AdocaoPrototipoForm(
                    data=dados_adocao(telefone=telefone)
                )

                self.assertTrue(form.is_valid(), form.errors)

    def test_telefones_invalidos(self):
        invalidos = [
            "((((((((((",
            "----------",
            "abc",
            "(17) 9999-000a",
            "17 99999.0000",
            "999990000",
            "179999900001",
            "+1 555 123 4567",
            "17+999990000",
        ]

        for telefone in invalidos:
            with self.subTest(telefone=telefone):
                form = AdocaoPrototipoForm(
                    data=dados_adocao(telefone=telefone)
                )

                self.assertIn("telefone", form.errors)


class AdocaoFluxoTests(TestCase):
    def setUp(self):
        self.client.force_login(criar_usuario())
        self.url = reverse("registrar_adocao")
        self.animal = Animal.objects.create(
            nome="Rex",
            especie=Animal.Especie.CAO,
            status=Animal.Status.DISPONIVEL,
        )

    def test_formulario_abre_com_aviso_de_dados_ficticios(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "fictícios e fixos no código")
        self.assertContains(resposta, "não consulta o banco de dados")

    def test_dados_invalidos_voltam_ao_formulario(self):
        resposta = self.client.post(
            self.url,
            dados_adocao(telefone="(((((((((("),
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("telefone", resposta.context["form"].errors)
        self.assertNotIn(CHAVE_SESSAO_RESULTADO, self.client.session)

    def test_simulacao_valida_mostra_resultado(self):
        resposta = self.client.post(self.url, dados_adocao())

        # fetch_redirect_response=False: abrir o resultado aqui já
        # limparia a sessão antes da verificação abaixo.
        self.assertRedirects(
            resposta,
            reverse("resultado_adocao"),
            fetch_redirect_response=False,
        )

        resultado = self.client.get(reverse("resultado_adocao"))

        self.assertContains(resultado, "Pessoa Fictícia")
        self.assertContains(resultado, "(17) 99999-0000")

    def test_resultado_limpa_dados_do_adotante_da_sessao(self):
        self.client.post(self.url, dados_adocao())
        self.assertIn(CHAVE_SESSAO_RESULTADO, self.client.session)

        self.client.get(reverse("resultado_adocao"))

        self.assertNotIn(CHAVE_SESSAO_RESULTADO, self.client.session)
        self.assertRedirects(
            self.client.get(reverse("resultado_adocao")),
            self.url,
        )

    def test_simulacao_nao_grava_nem_altera_animais(self):
        quantidade_antes = Animal.objects.count()
        atualizado_antes = self.animal.atualizado_em

        with CaptureQueriesContext(connection) as consultas:
            self.client.post(self.url, dados_adocao())
            self.client.get(reverse("resultado_adocao"))

        self.animal.refresh_from_db()
        self.assertEqual(Animal.objects.count(), quantidade_antes)
        self.assertEqual(self.animal.status, Animal.Status.DISPONIVEL)
        self.assertEqual(self.animal.atualizado_em, atualizado_antes)

        # Só a tabela de sessões do Django pode receber escrita.
        comandos_de_escrita = ("INSERT", "UPDATE", "DELETE")
        escritas = [
            consulta["sql"]
            for consulta in consultas.captured_queries
            if consulta["sql"].lstrip().upper().startswith(comandos_de_escrita)
            and "django_session" not in consulta["sql"]
        ]
        self.assertEqual(escritas, [])


class ConfiguracaoTests(SimpleTestCase):
    def test_env_bool_e_falso_por_padrao(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            self.assertFalse(env_bool("DEBUG"))

    def test_env_bool_reconhece_verdadeiro_e_falso(self):
        casos = {
            "True": True,
            "true": True,
            "1": True,
            "False": False,
            "0": False,
            "": False,
            "qualquer": False,
        }

        for valor, esperado in casos.items():
            with self.subTest(valor=valor):
                with mock.patch.dict("os.environ", {"DEBUG": valor}):
                    self.assertIs(env_bool("DEBUG"), esperado)

    def test_env_lista_separa_por_virgula(self):
        with mock.patch.dict(
            "os.environ",
            {"ALLOWED_HOSTS": " localhost, 127.0.0.1 ,,"},
        ):
            self.assertEqual(
                env_lista("ALLOWED_HOSTS"),
                ["localhost", "127.0.0.1"],
            )
