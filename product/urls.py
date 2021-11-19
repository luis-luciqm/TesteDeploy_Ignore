from django.shortcuts import render

# Create your views here.
from django.urls import path,include
from .views import *

urlpatterns = [
    #Product
    path('cadastrar_produto', ProductCreateView.as_view(), name='cadastrar_produto'),
    path('listar_produto/<str:option>/', ProductListView.as_view(), name='listar_produto'),
    path('detalhes/<slug:slug>/',ProductDetailSlugView.as_view(),name='lista_produto_slug'),
    path('editar_produto/<int:pk>/<str:option>/', ProductUpdateView.as_view(), name='editar_produto'),
    path('pendente_produto', PendenciesListView.as_view(), name='pendente_produto'),
    path('destaque_produto', hightlightListView.as_view(), name= 'destaque_produto'),
    path('generate_links_new/',gerar_link_ajax,name="generate_links_new"),
    path('remover_destaque/<int:pk>/', RemoveHighlightsView.as_view(), name='remover_destaque'),
    path('listar_produto_teste/', ProductListView.as_view(), name='listar_produto_teste'),
    path('listar_produto_pendente_ativo/', ActiveProductListView2.as_view(), name= 'listar_produto_pendente_ativo'),
    path('listar_produto_pendente_destaque/',HighlightProductListView2.as_view(), name= 'listar_produto_pendente_destaque'),
    path('detalhes_produto/<int:pk>/', ProductDetailView.as_view(), name='detalhes_produto'),
    path('resposta_comentario/<int:pk>/', addAnswerComment, name='resposta_comentario'),
    path('desativar_comentario/<int:id_comment>/<int:pk>/', DesactivateComment, name='desativar_comentario'),
    path('anuncios_comentados/', ProductCommentListView.as_view(), name= 'anuncios_comentados'),
    path('anuncios_reportados/', ProductReportListView.as_view(), name= 'anuncios_reportados'),
    path('marcar_resolvido/<int:pk>/', CheckedReportView.as_view(), name= 'marcar_resolvido'),
    path('marcar_todos_resolvido/', AllCheckedReportView.as_view(), name= 'marcar_todos_resolvido'),
    path('excluir_produto/<int:pk>/', DeleteProductView.as_view(), name = 'excluir_produto'),
    path('excluir_todos_pendentes/', DestroyAllProductsPending.as_view(), name='excluir_todos_pendentes'),
 
    path('acoes_tela_listagem/<int:pk>/<str:option>/', ActionProductListView.as_view(), name= 'acoes_tela_listagem'),
    path('abrir_posts/', productOpenAllReports, name='abrir_posts'),
    
]