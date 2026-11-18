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

class Adocao(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, related_name="adocoes")
    nome_adotante = models.CharField("Nome do adotante", max_length=120)
    telefone = models.CharField("Telefone", max_length=20)
    data = models.DateField("Data da adoção", default=timezone.localdate)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ["-data", "-pk"]
        constraints = [models.UniqueConstraint(fields=["animal"], condition=models.Q(ativa=True), name="uma_adocao_ativa_animal")]

    def __str__(self):
        return f"Adoção #{self.pk} — {self.animal}"


class Devolucao(models.Model):
    adocao = models.OneToOneField(Adocao, on_delete=models.PROTECT, related_name="devolucao")
    data = models.DateField("Data da devolução", default=timezone.localdate)
    motivo = models.TextField("Motivo")

    class Meta:
        ordering = ["-data", "-pk"]


class Lancamento(models.Model):
    tipo = models.CharField("Tipo", max_length=7, choices=[("doacao", "Doação"), ("despesa", "Despesa")])
    data = models.DateField("Data", default=timezone.localdate)
    valor = models.DecimalField("Valor (R$)", max_digits=12, decimal_places=2)
    descricao = models.CharField("Descrição", max_length=200)

    class Meta:
        ordering = ["-data", "-pk"]
        constraints = [models.CheckConstraint(condition=models.Q(valor__gt=0), name="lancamento_valor_positivo")]
