from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_artigos, name='listar_artigos'),
    path('criar/', views.criar_artigo, name='criar_artigo'),
    path('editar/<int:pk>/', views.editar_artigo, name='editar_artigo'),
    path('excluir/<int:pk>/', views.excluir_artigo, name='excluir_artigo'),
    path('visualizar/<int:pk>/', views.visualizar_artigo, name='visualizar_artigo'),
    path('buscar/', views.buscar_artigos, name='buscar_artigos'),
]
