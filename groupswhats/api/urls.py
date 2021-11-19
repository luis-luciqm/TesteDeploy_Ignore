from django.urls import path
from .viewsets import *

urlpatterns = [
    path('', GroupsWhatsViewSet.as_view(), name='listar_grupos'),
    path('listar_grupos_ativos/', GroupsWhatsActiveListViewSet.as_view(), name='listar_grupos_ativos'),
    path('editar_grupo/<str:pk>/',GroupWhatsEditViewSet.as_view(), name = 'editar_grupo'),
    path('remover_grupo/<str:pk>/', GroupWhatsDeleteViewSet.as_view(), name='remover_grupo'),
    path('criar_margem/', MarginCreateViewSet.as_view(), name='criar_margem'),
    path('listar_margens/',MarginListViewSet.as_view(), name='listar_margens'),
    path('editar_margem/<slug:slug>/', MarginEditViewSet.as_view(), name = 'editar_margem'),
    path('criar_mensagem/', MessageCreateViewSet.as_view(), name='criar_mensagem'),
    path('listar_mensagens/', MessageListViewSet.as_view(), name = 'listar_mensagens'),
]