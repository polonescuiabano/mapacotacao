# Generated by Django 5.0.2 on 2024-05-07 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapadecotacao', '0007_insumo_empresa_alter_preco_data_cotacao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='preco',
            name='nome_empresa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
