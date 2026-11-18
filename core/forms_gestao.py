import re
from django import forms
from django.utils import timezone
from .models import Animal, Adocao, Devolucao, Lancamento

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["aria-describedby"] = f"erro_{name}"
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(format="%Y-%m-%d", attrs={"type":"date", "class":"form-control", "aria-describedby":f"erro_{name}"})
                field.input_formats = ["%Y-%m-%d"]
            if self.is_bound:
                field.widget.attrs["aria-invalid"] = "true" if name in self.errors else "false"

    def clean(self):
        data = super().clean()
        for name in ("data", "data_entrada"):
            if data.get(name) and data[name] > timezone.localdate():
                self.add_error(name, "A data não pode ser futura.")
        return data

class AnimalForm(BaseForm):
    class Meta:
        model = Animal
        fields = ["nome", "especie", "porte", "data_entrada", "observacoes"]
        widgets = {"observacoes": forms.Textarea(attrs={"rows":3})}

class AdocaoForm(BaseForm):
    class Meta:
        model = Adocao
        fields = ["animal", "nome_adotante", "telefone", "data"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["animal"].queryset = Animal.objects.exclude(status=Animal.Status.ADOTADO).exclude(adocoes__ativa=True).distinct()
        self.fields["telefone"].widget.attrs.update({"inputmode":"tel", "autocomplete":"tel"})

    def clean_telefone(self):
        value = self.cleaned_data["telefone"].strip()
        if not re.fullmatch(r"\+?[0-9()\s-]+", value):
            raise forms.ValidationError("Informe um telefone válido com DDD.")
        digits = re.sub(r"\D", "", value)
        if value.startswith("+"):
            if not digits.startswith("55"):
                raise forms.ValidationError("Use um telefone brasileiro (+55).")
            digits = digits[2:]
        if len(digits) not in (10,11):
            raise forms.ValidationError("Informe o DDD e o número, com 10 ou 11 dígitos.")
        return value

class DevolucaoForm(BaseForm):
    class Meta:
        model = Devolucao
        fields = ["adocao", "data", "motivo"]
        widgets = {"motivo": forms.Textarea(attrs={"rows":3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["adocao"].queryset = Adocao.objects.filter(ativa=True).select_related("animal")

class LancamentoForm(BaseForm):
    class Meta:
        model = Lancamento
        fields = ["tipo", "data", "valor", "descricao"]

    def clean_valor(self):
        value = self.cleaned_data["valor"]
        if value <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        return value
