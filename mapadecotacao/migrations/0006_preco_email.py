# Generated by Django 5.0.2 on 2024-05-07 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapadecotacao', '0005_remove_insumo_cnpj_remove_insumo_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='preco',
            name='email',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]