from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET
from .models import Animal, Adocao, Devolucao, Lancamento
from .forms_gestao import AnimalForm, AdocaoForm, DevolucaoForm, LancamentoForm


def formulario(request, form, titulo):
    return render(request, "core/gestao_form.html", {"form":form, "titulo":titulo})

@login_required
@require_GET
def animais(request):
    busca = request.GET.get("q", "").strip()
    qs = Animal.objects.all()
    if busca:
        qs = qs.filter(nome__icontains=busca)
    return render(request, "core/gestao_animais.html", {"pagina":Paginator(qs,20).get_page(request.GET.get("page")), "busca":busca})

@login_required
@require_http_methods(["GET","POST"])
def animal_novo(request):
    form = AnimalForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        obj = form.save()
        return redirect("animal_detalhe", pk=obj.pk)
    return formulario(request, form, "Cadastrar animal")

@login_required
@require_GET
def animal_detalhe(request, pk):
    obj = get_object_or_404(Animal, pk=pk)
    return render(request, "core/gestao_animal.html", {"animal":obj})

@login_required
@require_http_methods(["GET","POST"])
def adocao_nova(request):
    form = AdocaoForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                animal = Animal.objects.select_for_update().get(pk=form.cleaned_data["animal"].pk)
                if animal.status == Animal.Status.ADOTADO or Adocao.objects.filter(animal=animal, ativa=True).exists():
                    form.add_error("animal", "Este animal já possui adoção ativa.")
                elif form.cleaned_data["data"] < animal.data_entrada:
                    form.add_error("data", "A adoção não pode ser anterior à entrada.")
                else:
                    obj = form.save(commit=False)
                    obj.animal = animal
                    obj.save()
                    animal.status = Animal.Status.ADOTADO
                    animal.save(update_fields=["status","atualizado_em"])
                    return redirect("adocao_detalhe", pk=obj.pk)
        except IntegrityError:
            form.add_error(None, "O registro foi alterado por outro acesso. Atualize e tente novamente.")
    return formulario(request, form, "Registrar adoção")

@login_required
@require_GET
def adocao_detalhe(request, pk):
    obj = get_object_or_404(Adocao.objects.select_related("animal"), pk=pk)
    return render(request, "core/gestao_adocao.html", {"adocao":obj})

@login_required
@require_GET
def adocoes(request):
    qs = Adocao.objects.select_related("animal")
    return render(request,"core/gestao_adocoes.html",{"pagina":Paginator(qs,20).get_page(request.GET.get("page"))})

@login_required
@require_http_methods(["GET","POST"])
def devolucoes(request):
    form = DevolucaoForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                adocao = Adocao.objects.select_for_update().get(pk=form.cleaned_data["adocao"].pk)
                animal = Animal.objects.select_for_update().get(pk=adocao.animal_id)
                if not adocao.ativa or Devolucao.objects.filter(adocao=adocao).exists():
                    form.add_error("adocao", "Esta adoção já foi encerrada.")
                elif form.cleaned_data["data"] < adocao.data:
                    form.add_error("data", "A devolução não pode ser anterior à adoção.")
                else:
                    obj = form.save(commit=False)
                    obj.adocao = adocao
                    obj.save()
                    adocao.ativa = False
                    adocao.save(update_fields=["ativa"])
                    animal.status = Animal.Status.ACOLHIDO
                    animal.save(update_fields=["status","atualizado_em"])
                    return redirect("devolucoes")
        except IntegrityError:
            form.add_error(None, "Não foi possível registrar. Atualize e tente novamente.")
    qs = Devolucao.objects.select_related("adocao__animal")
    return render(request,"core/gestao_devolucoes.html",{"form":form,"pagina":Paginator(qs,20).get_page(request.GET.get("page"))})

@login_required
@require_http_methods(["GET","POST"])
def financeiro(request):
    form = LancamentoForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("financeiro")
    qs = Lancamento.objects.all()
    entradas = qs.filter(tipo="doacao").aggregate(total=Sum("valor"))["total"] or Decimal("0")
    saidas = qs.filter(tipo="despesa").aggregate(total=Sum("valor"))["total"] or Decimal("0")
    return render(request,"core/gestao_financeiro.html",{"form":form,"pagina":Paginator(qs,20).get_page(request.GET.get("page")),"entradas":entradas,"saidas":saidas,"saldo":entradas-saidas})
