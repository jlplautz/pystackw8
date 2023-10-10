from django.urls import path

from . import views

urlpatterns = [
    path(
        'acesso_medico/<str:token>',
        views.acesso_medico,
        name='acesso_medico',
    ),
    path(
        'cancelar_pedido/<int:pedido_id>',
        views.cancelar_pedido,
        name='cancelar_pedido',
    ),
    path(
        'gerar_acesso_medico/',
        views.gerar_acesso_medico,
        name='gerar_acesso_medico',
    ),
    path('gerenciar_exames/', views.gerenciar_exames, name='gerenciar_exames'),
    path(
        'gerenciar_pedidos/',
        views.gerenciar_pedidos,
        name='gerenciar_pedidos',
    ),
    path('fechar_pedido/', views.fechar_pedido, name='fechar_pedido'),
    path('solicitar_exames/', views.solicitar_exames, name='solicitar_exames'),
    path(
        'solicitar_senha_exame/<int:exame_id>',
        views.solicitar_senha_exame,
        name='solicitar_senha_exame',
    ),
    path(
        'permitir_abrir_exame/<int:exame_id>',
        views.permitir_abrir_exame,
        name='permitir_abrir_exame',
    ),
]
