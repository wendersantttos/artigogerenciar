
from django.contrib import admin
from .models import Artigo, Revisao, PermissaoExclusao

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autores', 'revista', 'data', 'criado_em', 'modificado_em')
    search_fields = ('titulo', 'autores', 'revista')
    list_filter = ('revista', 'data')
    ordering = ('-data',)

@admin.register(Revisao)
class RevisaoAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'titulo_antigo', 'data_modificacao', 'modificado_por')
    search_fields = ('artigo__titulo', 'modificado_por__username')

@admin.register(PermissaoExclusao)
class PermissaoExclusaoAdmin(admin.ModelAdmin):
    list_display = ('user',)
