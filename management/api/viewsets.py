from rest_framework import generics
from .serializers import CategorySerializer, StoreSerializer, SubcategorySerializer
from management.models import *

#categorias
class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
   

    def get_queryset(self):    
        queryset = Category.objects.all()
        category = self.request.query_params.get('categoria')
        
        if category  is not None:
            queryset = queryset.filter(name=category)  
        return queryset

class CategoryListNoPagination(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):    
        queryset = Category.objects.all()
        category = self.request.query_params.get('categoria')
        
        if category  is not None:
            queryset = queryset.filter(name=category)  
        return queryset
    
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    
class CreateCategory(generics.CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
#subcategorias
class SubcategoryList(generics.ListAPIView):
    serializer_class = SubcategorySerializer
    queryset = SubCategory.objects.all()
    
class CreateSubCategory(generics.CreateAPIView):
    serializer_class = SubcategorySerializer
    queryset = SubCategory.objects.all()

# revisar  
class StoreListViewSet(generics.ListAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()

class StoreDetailViewSet(generics.RetrieveAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    lookup_field = "slug"

class StoreListViewSetNoPagination(generics.ListAPIView):

    pagination_class = None

    serializer_class = StoreSerializer
    queryset = Store.objects.all()
