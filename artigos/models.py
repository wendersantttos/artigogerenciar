from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Artigo(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    autores = models.CharField(max_length=255)
    resumo = models.TextField()
    abstract = models.TextField()
    palavras_chave = models.CharField(max_length=255)
    data = models.PositiveIntegerField()
    revista = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='artigos/', blank=True, null=True)
    sugestoes = models.TextField(blank=True, null=True)
    revisoes = models.ManyToManyField('Revisao', related_name='artigos', blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='artigos_criados')
    modificado_em = models.DateTimeField(auto_now=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    def clean(self):
        if len(self.resumo) > 1000:
            raise ValidationError("O resumo não pode ter mais de 1000 caracteres.")
        if len(self.abstract) > 1000:
            raise ValidationError("O abstract não pode ter mais de 1000 caracteres.")

    def save(self, *args, **kwargs):
        if self.pk:
            original = Artigo.objects.get(pk=self.pk)
            if original and (original.titulo != self.titulo or 
                             original.resumo != self.resumo or 
                             original.abstract != self.abstract):
                revisao = Revisao.objects.create(
                    artigo=self,
                    titulo_antigo=original.titulo,
                    resumo_antigo=original.resumo,
                    abstract_antigo=original.abstract,
                    modificado_por=self.criado_por
                )
                self.revisoes.add(revisao)
        super().save(*args, **kwargs)

    def pode_ser_excluido_por(self, user):
        return PermissaoExclusao.objects.filter(user=user).exists()

class Revisao(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='revisoes_relacionadas')
    titulo_antigo = models.CharField(max_length=255)
    resumo_antigo = models.TextField()
    abstract_antigo = models.TextField()
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='revisoes')
    data_modificacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revisão de {self.artigo.titulo} em {self.data_modificacao}"

class PermissaoExclusao(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='permissao_exclusao')

    def __str__(self):
        return f"Permissão de exclusão para {self.user.username}"
