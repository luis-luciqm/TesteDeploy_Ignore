from django.urls import path
from .viewsets import *


urlpatterns = [
    #categoria
    path('listar_categoria/', CategoryList.as_view()),
    path('listar_categoria_sem_paginacao/', CategoryListNoPagination.as_view()),
    path('categoria/<slug:slug>',CategoryDetailView.as_view()),
    
    path('listar_lojas/',StoreListViewSet.as_view(), name='listar_lojas'),
    path('listar_detalhes_loja/<slug:slug>/', StoreDetailViewSet.as_view(), name = 'listar_detalhes_loja'),
    path('listar_lojas_sem_paginacao/', StoreListViewSetNoPagination.as_view(), name = 'listar_lojas_sem_paginacao'),


]