# Generated by Django 5.0.2 on 2024-06-02 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapadecotacao', '0014_arquivoanexado_preco_delete_insumopendente'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapa',
            name='title',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
