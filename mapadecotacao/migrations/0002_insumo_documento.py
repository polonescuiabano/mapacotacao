# Generated by Django 5.0.2 on 2024-04-21 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapadecotacao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='insumo',
            name='documento',
            field=models.FileField(blank=True, null=True, upload_to='documentos/'),
        ),
    ]
