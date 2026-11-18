from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.login_view,
        name="login",
    ),
    path(
        "sair/",
        views.logout_view,
        name="logout",
    ),
    path(
        "menu/",
        views.menu_view,
        name="menu",
    ),
    path(
        "adocoes/nova/",
        views.registrar_adocao,
        name="registrar_adocao",
    ),
    path(
        "adocoes/resultado/",
        views.resultado_adocao,
        name="resultado_adocao",
    ),
    # Endpoint público de saúde — verifica apenas a aplicação.
    # Não executa consultas ao banco para não interferir com o
    # scale-to-zero do Neon Free. Ver core/views.py para detalhes.
    path(
        "health/",
        views.health_check,
        name="health_check",
    ),
]
