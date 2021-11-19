from django.db.models.base import Model
from django.http import request
from django.http.response import HttpResponse
import requests
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import permissions
from django.db.models import Q, query
from management.models import Category, Store, SubCategory,User
from rolepermissions.decorators import has_role_decorator
from rest_framework.filters import SearchFilter,OrderingFilter
import shutil
from product.utils import download_image
from product.models import Product, Comment, Report_Problem
from .serializers import ProductSetStatusSerializer, ProductUpdateTimeSerializer, ProductSendTelegramSerializer, ProductSendWhatsAppSerializer, ProductSendInstagramSerializer, ProductSendFacebookSerializer, BaseProductSerializer, ProductAddRelevantSerializer, ProductAddLikeSerializer, ProductAddExclusiveSerializer, ProductSerializer, CommentSerializer, ReportProblemSerializer, ProductLinkSerializer, SubCategoriaSerializer, CommentLikeSerializer
import io
from datetime import datetime
from rest_framework.exceptions import ParseError
from product.views import generate_link_curto, generate_linK_id_parceiro, push_notification
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 5),name='dispatch')
class ProdutoList(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title','description','subcategory__name','subcategory__category__name' )

    def get_queryset(self):    
        queryset = Product.objects.filter(Q(status='ACTIVE') | Q(status='CLOSED')).order_by('-created_at')
        return queryset

class ProdutoListActive(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title','description','subcategory__name','subcategory__category__name' )

    def get_queryset(self):    
        queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
        return queryset


class ProdutoByCategoriaSlugView(generics.ListAPIView):

    serializer_class = ProductSerializer
   
    def get_queryset(self):    
        queryset = Product.objects.all().order_by('-created_at').exclude(status='PENDING')
        slug = self.kwargs['slug']
       
        if slug is not None:
            queryset = queryset.filter(subcategory__category__slug=slug)  
        return queryset

class ProdutoBySubCategoriaSlugView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):    
        queryset = Product.objects.all().order_by('-created_at')
        slug = self.kwargs['slug']
       
        if slug is not None:
            queryset = queryset.filter(subcategory__slug=slug)  
        return queryset

##Nome, link, descrição, categoria, subcategoria, loja, preço antigo, preço na promoção, cupom, forma de pagamento e o link das imagens
class ProductCreateView2(generics.CreateAPIView):
    serializer_class = ProductSerializer
    
    def create(self, request, *args, **kwargs):
             
        url = request.data['image_url']
        file_name = url.split('/')[-1]
        
        res = requests.get(url, stream = True)

        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f) 
            print('Image sucessfully Downloaded: ',file_name)
        else:
            print('Image Couldn\'t be retrieved') 
        print(f)       
        
        request.data._mutable = True
        request.data['image']=f
        request.data._mutable = False
      
        return super().create(request, *args, **kwargs)

class ProductCreateView(APIView):
     
    def post(self, request, format=None):
        url = request.data['image_url']
        serializer = ProductSerializer(data=request.data)
      
        if serializer.is_valid():
            obj = serializer.save()
            
            if url:
                image =download_image(url,obj.slug) 
                obj.image = image
                obj.long_url = generate_linK_id_parceiro(obj.long_url)
                if obj.long_url == '':
                        raise ParseError({"error": "Este link não corresponde a nenhuma das lojas cadastradas"})
                
                obj.short_url = generate_link_curto(obj.long_url)
                obj.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailsSlugView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductDetailsView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ProductAddLikeView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProductAddLikeSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        product = self.get_object()

        if product.likes.filter(id=request.user.id).exists():
            product.likes.remove(request.user)
        else:
            product.likes.add(request.user)
        
        serializer= self.get_serializer(product,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"like successfully"})
        else:
            return Response({"error": serializer.errors})
class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentsListBySlugProduct(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(product__slug = self.kwargs['product_slug']).order_by('-created')
        return queryset

class CreateComment(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
#Reports
class CreateReportProblem (generics.CreateAPIView):
    serializer_class = ReportProblemSerializer
    
class ReportProblemList(generics.ListAPIView):
    queryset = Report_Problem.objects.filter(checked=False)
    serializer_class = ReportProblemSerializer

# Revisar todos a baixo 
class ProductSearchByWordViewSet(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.filter(status = 'ACTIVE', title__icontains = self.kwargs['title']) 
        return products
    
class SubCategoryListBySlug(generics.RetrieveAPIView):
    serializer_class = SubCategoriaSerializer
    queryset = SubCategory.objects.all()
    lookup_field = "slug"
class ProductListByStore(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.filter(Q(status='ACTIVE') | Q(status='CLOSED'), store_id = self.kwargs['pk_store'])
        return products

class ProductListByCoupon(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.exclude(coupon = '').filter(active = True)
        return products

class ProductGetLinkById(generics.ListAPIView):
    serializer_class = ProductLinkSerializer

    def get_queryset(self):
        try:
            products = Product.objects.filter(pk = self.kwargs['pk'])
            return products
        except:
            pass

class ProductVerifyNew(generics.ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        products = Product.objects.filter(status='ACTIVE').order_by('-created_at')[:1]
        return products

class CommentAddLikeView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentLikeSerializer
    queryset = Comment.objects.all()
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        
        serializer= self.get_serializer(comment,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"like successfully"})
        else:
            return Response({"error": serializer.errors})

#revisar

class ProductSentWhatsappViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSendWhatsAppSerializer
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        product = self.get_object()
        product.whatsapp = True
        serializer= self.get_serializer(product,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Produto enviado para o whatsapp"})
        else:
            return Response({"error": serializer.errors})

class ProductSentFacebookViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSendFacebookSerializer
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        product = self.get_object()
        product.facebook = True
        serializer= self.get_serializer(product,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Produto enviado para o facebook"})
        else:
            return Response({"error": serializer.errors})


class ProductSentTelegramViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSendTelegramSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        product = self.get_object()

        product.telegram = True
        serializer = self.get_serializer(product,data=request.data,partial=True)  
        
        if serializer.is_valid():
            serializer.save()      
            return Response({"message": "Produto enviado para o Telegram"})
        else:
            return Response({"error": serializer.errors})

class ProductSentInstagramViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSendInstagramSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        product = self.get_object()

        product.instagram = True
        serializer = self.get_serializer(product,data=request.data,partial=True)  
        
        if serializer.is_valid():
            serializer.save()      
            return Response({"message": "Produto enviado para o Instagram"})
        else:
            return Response({"error": serializer.errors})

class ProductUpdateTimeViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductUpdateTimeSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        product = self.get_object()

        if product.status == "CLOSED":
            product.status = "ACTIVE"
        else:
            product.created_at = datetime.today()
        
        serializer = self.get_serializer(product,data=request.data,partial=True)
        
        if serializer.is_valid():
            push_notification(product)
            serializer.save()      
            return Response({"message": "Promoção subida com sucesso"})
        else:
            return Response({"error": serializer.errors})

class ProductAddRelevantViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductAddRelevantSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        product = self.get_object()

        if product.relevant:
            product.relevant = False
        else:
            product.relevant = True
    
        serializer = self.get_serializer(product,data=request.data,partial=True)  
        
        if serializer.is_valid():
            serializer.save()  
            if product.relevant:   
                return Response({"message": "Promoção destacada com sucesso"})
            return Response({"message": "Promoção removida dos destaques"})
        else:
            raise ParseError({"error": serializer.errors})

class ProductClosedViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSetStatusSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        product = self.get_object()

        if product.exclusive:
            product.exclusive = False
            product.relevant = True
            product.status = "CLOSED"
        else:
            if product.status == "CLOSED":
                product.status = "ACTIVE"
            else:
                product.status = "CLOSED"
                if product.relevant:
                    product.relevant = False

        serializer = self.get_serializer(product,data=request.data,partial=True)  
        
        if serializer.is_valid():
            serializer.save()
            if product.status == "ACTIVE":  
                return Response({"message": "A promoção estava encerrada, e agora foi ativada novamente com sucesso"})
            else:   
                return Response({"message": "Promoção encerrada com sucesso"})
        else:
            return Response({"error": serializer.errors})

class ProductListRelevantAndExclusive(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(Q(relevant = True) | Q(exclusive = True)).order_by('-created_at')

class ProductAddExclusiveViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductAddExclusiveSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        products = Product.objects.filter(exclusive = True).count()
        product = self.get_object()

        if product.exclusive:
            product.exclusive = False
        else:
            if products >= 6:
                raise ParseError({"error": "Já existe 6 produtos exclusivos, para prosseguir remova algum deles"})
            else:
                product.exclusive = True
    
        serializer = self.get_serializer(product,data=request.data,partial=True)  
        
        if serializer.is_valid():
            serializer.save()   
            if not product.exclusive:
                return Response({"message": "Promoção removida dos exclusivos"})
            return Response({"message": "Esta promoção agora é exclusiva"})
        else:
            raise ParseError({"error": serializer.errors})

class ProductListExclusive(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(Q(status='ACTIVE') & Q(exclusive=True))
    
    

                
    




       