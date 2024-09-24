# Generated by Django 5.0.2 on 2024-03-29 22:42

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='djangoProject.empresa')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomUserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUserPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.permission')),
            ],
        ),
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('aprovado', models.BooleanField(default=False)),
                ('preco1', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cnpj1', models.CharField(max_length=20)),
                ('razao_social1', models.CharField(max_length=100)),
                ('data_cotacao1', models.DateField()),
                ('vendedor1', models.CharField(max_length=100)),
                ('telefone1', models.CharField(max_length=20)),
                ('status_preco1', models.CharField(blank=True, max_length=20, null=True)),
                ('preco2', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cnpj2', models.CharField(max_length=20)),
                ('razao_social2', models.CharField(max_length=100)),
                ('data_cotacao2', models.DateField()),
                ('vendedor2', models.CharField(max_length=100)),
                ('telefone2', models.CharField(max_length=20)),
                ('status_preco2', models.CharField(blank=True, max_length=20, null=True)),
                ('preco3', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cnpj3', models.CharField(max_length=20)),
                ('razao_social3', models.CharField(max_length=100)),
                ('data_cotacao3', models.DateField()),
                ('vendedor3', models.CharField(max_length=100)),
                ('telefone3', models.CharField(max_length=20)),
                ('status_preco3', models.CharField(blank=True, max_length=20, null=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insumos', to='djangoProject.empresa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AvaliacaoInsumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aprovado', models.BooleanField(default=False)),
                ('avaliador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoProject.insumo')),
            ],
        ),
        migrations.CreateModel(
            name='InsumoPendente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aprovado', models.BooleanField(default=False)),
                ('avaliador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoProject.insumo')),
            ],
        ),
    ]
