from django.urls import path
from . import views, views_animais

urlpatterns = [
    path("", views.login_view, name="login"),
    path("sair/", views.logout_view, name="logout"),
    path("menu/", views.menu_view, name="menu"),
    path("adocoes/nova/", views.registrar_adocao, name="registrar_adocao"),
    path("adocoes/resultado/", views.resultado_adocao, name="resultado_adocao"),
    path("health/", views.health_check, name="health_check"),
    path("animais/", views_animais.animais_lista, name="animais_lista"),
    path("animais/novo/", views_animais.animal_novo, name="animal_novo"),
    path("animais/<int:pk>/", views_animais.animal_detalhe, name="animal_detalhe"),
]
