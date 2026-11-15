from django.db import models
from django.utils import timezone


class Animal(models.Model):
    class Especie(models.TextChoices):
        CAO = "cao", "Cão"
        GATO = "gato", "Gato"
        OUTRO = "outro", "Outro"

    class Porte(models.TextChoices):
        PEQUENO = "pequeno", "Pequeno"
        MEDIO = "medio", "Médio"
        GRANDE = "grande", "Grande"
        NAO_INFORMADO = "nao_informado", "Não informado"

    class Status(models.TextChoices):
        ACOLHIDO = "acolhido", "Acolhido"
        DISPONIVEL = "disponivel", "Disponível para adoção"
        ADOTADO = "adotado", "Adotado"

    nome = models.CharField("Nome", max_length=100)
    especie = models.CharField(
        "Espécie",
        max_length=10,
        choices=Especie.choices,
    )
    porte = models.CharField(
        "Porte",
        max_length=15,
        choices=Porte.choices,
        default=Porte.NAO_INFORMADO,
    )
    data_entrada = models.DateField(
        "Data de entrada",
        default=timezone.localdate,
    )
    status = models.CharField(
        "Situação",
        max_length=15,
        choices=Status.choices,
        default=Status.ACOLHIDO,
    )
    observacoes = models.TextField(
        "Observações",
        blank=True,
    )
    criado_em = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
    )
    atualizado_em = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"
        ordering = ["nome", "pk"]

    def __str__(self):
        return f"{self.nome} — {self.get_especie_display()}"