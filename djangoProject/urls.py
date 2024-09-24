
from django.contrib import admin
from django.urls import path, include
from .views import profile, relatorios, cadastrar_insumos, gerar_relatorio
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import custom_logout






urlpatterns = [
    path('', profile, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', profile, name='user_profile'),
    path('relatorios/', relatorios, name='relatorios'),
    path('gerar_relatorio/', gerar_relatorio, name='gerar_relatorio'),
    path('cadastrar_insumos/', cadastrar_insumos, name='cadastrar_insumos'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('insumos_para_avaliar/', views.insumos_para_avaliar, name='insumos_para_avaliar'),
    path('avaliar_insumo/<int:insumo_id>/', views.avaliar_insumo, name='avaliar_insumo'),
    path('group/<str:group_name>/', views.user_list_by_group, name='user_list_by_group'),
    path('cadastrar-orcamento/', views.cadastrar_orcamento, name='cadastrar_orcamento'),
    path('delete_insumo/<int:insumo_id>/', views.delete_insumo, name='delete_insumo'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('rename-map-title/<int:mapa_id>/', views.rename_map_title, name='rename_map_title'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

