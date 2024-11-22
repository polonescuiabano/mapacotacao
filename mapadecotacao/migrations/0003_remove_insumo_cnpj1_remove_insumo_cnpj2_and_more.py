# Generated by Django 5.0.2 on 2024-04-21 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapadecotacao', '0002_insumo_documento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insumo',
            name='cnpj1',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='cnpj2',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='cnpj3',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='data_cotacao1',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='data_cotacao2',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='data_cotacao3',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='preco1',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='preco2',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='preco3',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='razao_social1',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='razao_social2',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='razao_social3',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='status_preco1',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='status_preco2',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='status_preco3',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='telefone1',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='telefone2',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='telefone3',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='vendedor1',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='vendedor2',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='vendedor3',
        ),
        migrations.CreateModel(
            name='ContatoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_vendedor', models.CharField(max_length=100)),
                ('telefone_vendedor', models.CharField(max_length=20)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapadecotacao.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Preco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cnpj', models.CharField(max_length=20)),
                ('razao_social', models.CharField(max_length=100)),
                ('data_cotacao', models.DateField()),
                ('vendedor', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=20)),
                ('status_preco', models.CharField(blank=True, max_length=20, null=True)),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='precos', to='mapadecotacao.insumo')),
            ],
        ),
    ]