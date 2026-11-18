from django.urls import path
from . import views, views_gestao as gestao

urlpatterns = [
    path("", views.login_view, name="login"),
    path("sair/", views.logout_view, name="logout"),
    path("menu/", views.menu_view, name="menu"),
    path("health/", views.health_check, name="health_check"),
    path("animais/", gestao.animais, name="animais_lista"),
    path("animais/novo/", gestao.animal_novo, name="animal_novo"),
    path("animais/<int:pk>/", gestao.animal_detalhe, name="animal_detalhe"),
    path("adocoes/", gestao.adocoes, name="adocoes_lista"),
    path("adocoes/nova/", gestao.adocao_nova, name="registrar_adocao"),
    path("adocoes/resultado/", gestao.adocoes, name="resultado_adocao"),
    path("adocoes/<int:pk>/", gestao.adocao_detalhe, name="adocao_detalhe"),
    path("devolucoes/", gestao.devolucoes, name="devolucoes"),
    path("financeiro/", gestao.financeiro, name="financeiro"),
]
