# Generated by Django 5.0.2 on 2024-04-21 22:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapadecotacao', '0003_remove_insumo_cnpj1_remove_insumo_cnpj2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insumo',
            name='aprovado',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='documento',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='insumo',
            name='user',
        ),
        migrations.AddField(
            model_name='insumo',
            name='cnpj',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='insumo',
            name='codigo',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='insumo',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='insumo',
            name='empresa_nome',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='insumo',
            name='preco',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='insumo',
            name='telefone',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='insumo',
            name='unidade_medida',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ArquivoAnexado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='arquivos_anexados/')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapadecotacao.empresa')),
            ],
        ),
    ]
