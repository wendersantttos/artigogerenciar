# forms.py
from django import forms
from .models import Artigo

class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'autores', 'resumo', 'abstract', 'palavras_chave', 'data', 'revista', 'arquivo', 'sugestoes']

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 5:
            raise forms.ValidationError("O título deve ter pelo menos 5 caracteres.")
        return titulo

    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data < 1900 or data > 2100:
            raise forms.ValidationError("A data deve estar entre 1900 e 2100.")
        return data

    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo and arquivo.size > 10 * 1024 * 1024:  # Limite de 10 MB
            raise forms.ValidationError("O arquivo não pode ter mais que 10 MB.")
        return arquivo
