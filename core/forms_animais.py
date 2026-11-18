from django import forms
from django.utils import timezone
from .models import Animal


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ["nome", "especie", "porte", "data_entrada", "observacoes"]
        widgets = {
            "data_entrada": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "observacoes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data_entrada"].input_formats = ["%Y-%m-%d"]
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["aria-describedby"] = f"ajuda_{name} erro_{name}"
            if self.is_bound:
                field.widget.attrs["aria-invalid"] = "false"
        if self.is_bound:
            for name in self.errors:
                if name in self.fields:
                    self.fields[name].widget.attrs["aria-invalid"] = "true"

    def clean_data_entrada(self):
        value = self.cleaned_data["data_entrada"]
        if value > timezone.localdate():
            raise forms.ValidationError("A data de entrada não pode ser futura.")
        return value
