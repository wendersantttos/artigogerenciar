# Generated by Django 5.1.1 on 2024-09-09 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('autores', models.CharField(max_length=300)),
                ('resumo', models.TextField()),
                ('abstract', models.TextField()),
                ('palavras_chave', models.CharField(max_length=200)),
                ('data', models.PositiveIntegerField()),
                ('revista', models.CharField(max_length=200)),
                ('arquivo', models.FileField(upload_to='artigos/')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]