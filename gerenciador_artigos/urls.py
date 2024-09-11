"""
URL configuration for gerenciador_artigos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from artigos import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # URL para o admin do Django
    path('login/', auth_views.LoginView.as_view(template_name='artigos/login.html'), name='login'),  # URL para a página de login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # URL para o logout
    path('', views.listar_artigos, name='listar_artigos'),  # URL para listar artigos
    path('criar/', views.criar_artigo, name='criar_artigo'),  # URL para criar um novo artigo
    path('editar/<int:pk>/', views.editar_artigo, name='editar_artigo'),  # URL para editar um artigo existente
    path('excluir/<int:pk>/', views.excluir_artigo, name='excluir_artigo'),  # URL para excluir um artigo
    path('visualizar/<int:pk>/', views.visualizar_artigo, name='visualizar_artigo'),  # URL para visualizar detalhes de um artigo
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve arquivos de mídia durante o desenvolvimento

