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
]