from django.urls import path
from .viewsets import *

  

urlpatterns = [
    
    path('',ProdutoList.as_view(),name="api-lista-produtos"), 
    path('ativas/',ProdutoListActive.as_view(),name="api-lista-produtos-ativas"),

    path('categoria/<slug:slug>',ProdutoByCategoriaSlugView.as_view(),name="api-lista-produto-categoria"),
    path('subcategoria/<slug:slug>',ProdutoBySubCategoriaSlugView.as_view(),name="api-lista-produto-subcategoria"),

    path('detalhe/<slug:slug>',ProductDetailsSlugView.as_view(),name="api-detalhe-produto"),
    path('destaques/',ProductListRelevantAndExclusive.as_view(),name="api-lista-destaques"),
    path('curtir/<int:pk>',ProductAddLikeView.as_view(),name="curtir-produto"),

    #extensão chrome
    path('criar_anuncio/',ProductCreateView.as_view(),name="api-criar-anuncio"),
   
    path('listar_comentarios/', CommentList.as_view(), name = 'listar_comentarios'),
    path('criar_comentario/', CreateComment.as_view(), name = 'criar_comentario'),
    path('listar_comentario_produto/<slug:product_slug>/', CommentsListBySlugProduct.as_view(), name = 'listar_comentario_produto'),
    path('curtir_comentario/<int:pk>', CommentAddLikeView.as_view(), name = 'curtir_comentario_produto'),


    path('reportar_problema/', CreateReportProblem.as_view(), name = 'reportar_problema'),
    path('listar_reportados/', ReportProblemList.as_view(), name = 'listar_reportados'),

    #revisar todos a baixo
    path('listar_produto_por_palavra/<str:title>/', ProductSearchByWordViewSet.as_view(), name = 'listar_produto_por_palavra'),
    path('pegar_subcategoria_slug/<slug:slug>/', SubCategoryListBySlug.as_view(), name = 'pegar_subcategoria_slug'),
    path('listar_produto_por_loja/<int:pk_store>/', ProductListByStore.as_view(), name = 'listar_produto_por_loja'),
    path('listar_produto_cupon/', ProductListByCoupon.as_view(), name = 'listar_produto_cupon'),
    path('pegar_link_produto/<int:pk>/', ProductGetLinkById.as_view(), name = 'pegar_link_produto'),
    path('pegar_ultimo_produto/', ProductVerifyNew.as_view(), name = 'pegar_ultimo_produto'), 
    
    path('produto_enviado_whatsapp/<int:pk>/', ProductSentWhatsappViewSet.as_view(), name = 'produto_enviado_whatsapp'),
    path('produto_enviado_facebook/<int:pk>/', ProductSentFacebookViewSet.as_view(), name = 'produto_enviado_facebook'),
    path('produto_enviado_instagram/<int:pk>/', ProductSentInstagramViewSet.as_view(), name = 'produto_enviado_instagram'),
    path('produto_enviado_telegram/<int:pk>/', ProductSentTelegramViewSet.as_view(), name = 'produto_enviado_telegram'),
    
    path('subir_promocao/<int:pk>/', ProductUpdateTimeViewSet.as_view(), name = 'subir_promocao'),   
    path('destacar_promocao/<int:pk>/', ProductAddRelevantViewSet.as_view(), name = 'destacar_promocao'),
    path('encerrar_promocao/<int:pk>/', ProductClosedViewSet.as_view(), name = 'encerrar_promocao'),
    path('adicionar_exclusivo_produto/<int:pk>/', ProductAddExclusiveViewSet.as_view(), name= 'adicionar_exclusivo'),
    # path('produtos_com_mais_curtidas/', ProductsMostLikes.as_view(), name='produtos_com_mais_curtidas'),
    path('listar_exclusivas/', ProductListExclusive.as_view(), name='listar_exclusivas'),
    
]