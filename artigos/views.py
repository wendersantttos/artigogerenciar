from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q  # Import necessário para usar o Q object
from .models import Artigo, Revisao
from .forms import ArtigoForm

@login_required
def listar_artigos(request):
    query = request.GET.get('q', '')
    order = request.GET.get('o', 'titulo')  # Define a ordenação padrão por título
    artigos = Artigo.objects.all()
    
    if query:
        # Filtrar com Q object para permitir busca em diferentes critérios
        artigos = artigos.filter(
            Q(titulo__icontains=query) |
            Q(autores__icontains=query) |
            Q(revista__icontains=query) |
            Q(palavras_chave__icontains=query) |
            Q(resumo__icontains=query) |
            Q(abstract__icontains=query) |
            Q(data__icontains=query)
        )
    
    # Ordenar os resultados com base na ordenação selecionada
    if order in ['titulo', 'autores', 'revista', 'data']:
        artigos = artigos.order_by(order)
    else:
        artigos = artigos.order_by('titulo')  # Ordem padrão por título se a ordenação for inválida
    
    # Implementar a paginação
    paginator = Paginator(artigos, 10)  # 10 artigos por página
    page_number = request.GET.get('page')
    artigos_page = paginator.get_page(page_number)
    
    return render(request, 'artigos/lista.html', {
        'artigos': artigos_page,
        'query': query,
        'order': order
    })

@login_required
def criar_artigo(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_artigos')
    else:
        form = ArtigoForm()
    return render(request, 'artigos/form.html', {'form': form})

@login_required
def editar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES, instance=artigo)
        if form.is_valid():
            old_data = {
                'titulo': artigo.titulo,
                'autores': artigo.autores,
                'resumo': artigo.resumo,
                'abstract': artigo.abstract,
                'palavras_chave': artigo.palavras_chave,
                'data': artigo.data,
                'revista': artigo.revista,
                'arquivo': artigo.arquivo,
                'sugestoes': artigo.sugestoes
            }
            artigo = form.save()
            new_data = {
                'titulo': artigo.titulo,
                'autores': artigo.autores,
                'resumo': artigo.resumo,
                'abstract': artigo.abstract,
                'palavras_chave': artigo.palavras_chave,
                'data': artigo.data,
                'revista': artigo.revista,
                'arquivo': artigo.arquivo,
                'sugestoes': artigo.sugestoes
            }
            for campo, valor_antigo in old_data.items():
                valor_novo = new_data[campo]
                if valor_antigo != valor_novo:
                    Revisao.objects.create(
                        artigo=artigo,
                        usuario=request.user,
                        campo=campo,
                        valor_antigo=valor_antigo,
                        valor_novo=valor_novo
                    )
            return redirect('listar_artigos')
    else:
        form = ArtigoForm(instance=artigo)
    return render(request, 'artigos/form.html', {'form': form})

@login_required
def excluir_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if not artigo.pode_ser_excluido_por(request.user):
        return HttpResponseForbidden("Você não tem permissão para excluir este artigo.")
    if request.method == 'POST':
        artigo.delete()
        return redirect('listar_artigos')
    return render(request, 'artigos/confirmar_exclusao.html', {'artigo': artigo})

@login_required
def visualizar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    return render(request, 'artigos/detalhes.html', {'artigo': artigo})
