from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    
    #CRUD DE LOJAS
    path('cadastro_lojas', StoreCreateView.as_view(), name='cadastro_lojas'),
    path('lista_lojas', StoreListView.as_view(), name= 'lista_lojas'),
    path('editar_loja/<int:pk>/', StoreEditView.as_view(), name='editar_loja'),
    path('desativar_loja/<int:pk>/', StoreDisableView.as_view(), name='desativar_loja'),
    path('ativar_loja/<int:pk>/', StoreActivateView.as_view(), name='ativar_loja'),
    path('listagem_usuario/', FuncListView.as_view(), name='listagem_usuario'),
    path('editar_usuario/<int:pk>/',  UserEditView.as_view(), name='editar_usuario'),
    path('get_categoria_ajax/', get_categoria_ajax, name="get_categoria_ajax"),
    path('desativar_usuario/<int:pk>/', UserDisableView.as_view(), name='desativar_usuario'),
    path('ativar_usuario/<int:pk>/', UserEnableView.as_view(), name='ativar_usuario'),
]
