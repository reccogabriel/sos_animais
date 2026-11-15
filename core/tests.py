from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from .models import Animal


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