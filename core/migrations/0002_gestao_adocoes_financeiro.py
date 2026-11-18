from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [("core", "0001_cria_modelo_animal")]
    operations = [
        migrations.CreateModel(name='Adocao', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('nome_adotante', models.CharField(max_length=120, verbose_name='Nome do adotante')), ('telefone', models.CharField(max_length=20, verbose_name='Telefone')), ('data', models.DateField(default=django.utils.timezone.localdate, verbose_name='Data da adoção')), ('ativa', models.BooleanField(default=True)), ('animal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adocoes', to='core.animal'))], options={"ordering":["-data","-pk"]}),
        migrations.CreateModel(name='Devolucao', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('data', models.DateField(default=django.utils.timezone.localdate, verbose_name='Data da devolução')), ('motivo', models.TextField(verbose_name='Motivo')), ('adocao', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='devolucao', to='core.adocao'))], options={"ordering":["-data","-pk"]}),
        migrations.CreateModel(name='Lancamento', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('tipo', models.CharField(choices=[('doacao','Doação'),('despesa','Despesa')], max_length=7, verbose_name='Tipo')), ('data', models.DateField(default=django.utils.timezone.localdate, verbose_name='Data')), ('valor', models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor (R$)')), ('descricao', models.CharField(max_length=200, verbose_name='Descrição'))], options={"ordering":["-data","-pk"]}),
        migrations.AddConstraint(model_name="adocao", constraint=models.UniqueConstraint(fields=["animal"], condition=models.Q(ativa=True), name="uma_adocao_ativa_animal")),
        migrations.AddConstraint(model_name="lancamento", constraint=models.CheckConstraint(condition=models.Q(valor__gt=0), name="lancamento_valor_positivo")),
    ]
