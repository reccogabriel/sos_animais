from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_GET
from .forms_animais import AnimalForm
from .models import Animal


@login_required
@require_GET
def animais_lista(request):
    busca = request.GET.get("q", "").strip()
    animais = Animal.objects.all().order_by("nome", "pk")
    if busca:
        animais = animais.filter(nome__icontains=busca)
    pagina = Paginator(animais, 20).get_page(request.GET.get("page"))
    return render(request, "core/animais_lista.html", {"pagina": pagina, "busca": busca})


@login_required
@require_http_methods(["GET", "POST"])
def animal_novo(request):
    form = AnimalForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        animal = form.save()
        return redirect("animal_detalhe", pk=animal.pk)
    return render(request, "core/animal_form.html", {"form": form})


@login_required
@require_GET
def animal_detalhe(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, "core/animal_detalhe.html", {"animal": animal})
