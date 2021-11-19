from management.models import Category, Store, SubCategory
from rest_framework import serializers
from management.models import Form_Payment
from product.models import Product, Comment, Report_Problem
from authentication.models import User
from management.api.serializers import StoreSerializer, SubcategorySerializer,Freight


class UserSereializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','image')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSereializer(required=False)
    number_of_likes =serializers.IntegerField(read_only=True)
    class Meta:
        model = Comment
        fields = ('__all__')
        
class CommentLikeSerializer(serializers.ModelSerializer):
    author = UserSereializer(read_only=True)
    number_of_likes =serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True)
    active = serializers.BooleanField(read_only=True)
    created = serializers.DateField(read_only=True)
    parent = CommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('__all__')

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')

class SubCategoriaSerializer(serializers.ModelSerializer):

    category = CategoriaSerializer()
    class Meta:
        model = SubCategory
        fields = ('__all__')

class BaseProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    old_price = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    price = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    image = serializers.ImageField(read_only=True)

    image_social = serializers.ImageField(read_only=True)
    status = serializers.CharField(read_only=True)
    long_url = serializers.URLField(read_only=True)
    short_url = serializers.CharField(read_only=True)

    coupon = serializers.CharField(read_only=True)
    relevant = serializers.BooleanField(read_only=True)
    exclusive = serializers.BooleanField(read_only=True)
    active = serializers.BooleanField(read_only=True)

    whatsapp = serializers.BooleanField(read_only=True)
    telegram = serializers.BooleanField(read_only=True)
    instagram = serializers.BooleanField(read_only=True)
    facebook = serializers.BooleanField(read_only=True)

    store = StoreSerializer(required=False, read_only=True)
    freight = serializers.SlugRelatedField(read_only=True,slug_field='name')
    warning = serializers.SlugRelatedField(read_only=True,slug_field='name')
    created_at = serializers.DateTimeField(read_only=True)
    user = UserSereializer(required=False, read_only=True)
    subcategory = SubCategoriaSerializer(read_only=True)

    form_payment = serializers.SlugRelatedField(queryset=Form_Payment.objects.all(),slug_field='name')
    user_id = serializers.IntegerField(read_only=True)
    store_id = serializers.IntegerField(default=1, read_only=True)
    number_of_likes = serializers.IntegerField(read_only=True)
    total_comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        exclude = ('updated_at',)

    def get_total_comment(self,Product):
        return Product.comments.count()


class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(required=False)
    subcategory = SubcategorySerializer(required=False)
    freight = serializers.SlugRelatedField(queryset=Freight.objects.all(),slug_field='name')
    warning = serializers.SlugRelatedField(read_only=True,slug_field='name')
    created_at = serializers.DateTimeField(read_only=True)
    user = UserSereializer(required=False)
    subcategory = SubCategoriaSerializer(read_only=True)

    form_payment = serializers.SlugRelatedField(queryset=Form_Payment.objects.all(),slug_field='name')
    user_id = serializers.IntegerField()
    store_id = serializers.IntegerField()
    subcategory_id = serializers.IntegerField()
    number_of_likes =serializers.IntegerField(read_only=True)
    total_comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        exclude = ('updated_at',)

    def get_total_comment(self,Product):
        return Product.comments.count()

# revisar  
class ProductAddExclusiveSerializer(BaseProductSerializer, serializers.ModelSerializer):
    exclusive = serializers.BooleanField(read_only=False) 

class ProductAddLikeSerializer(BaseProductSerializer, serializers.ModelSerializer):
    pass    

class ProductAddRelevantSerializer(BaseProductSerializer, serializers.ModelSerializer):
    relevant = serializers.BooleanField(read_only=False) 

class ProductSendFacebookSerializer(BaseProductSerializer, serializers.ModelSerializer):
    facebook = serializers.BooleanField(read_only=False)

class ProductSendInstagramSerializer(BaseProductSerializer, serializers.ModelSerializer):
    instagram = serializers.BooleanField(read_only=False)

class ProductSendWhatsAppSerializer(BaseProductSerializer, serializers.ModelSerializer):
    whatsapp = serializers.BooleanField(read_only=False)

class ProductSendTelegramSerializer(BaseProductSerializer, serializers.ModelSerializer):
    telegram = serializers.BooleanField(read_only=False)

class ProductUpdateTimeSerializer(BaseProductSerializer, serializers.ModelSerializer):
    created_at = serializers.BooleanField(read_only=False)

class ProductSetStatusSerializer(BaseProductSerializer, serializers.ModelSerializer):
    status = serializers.CharField(read_only=False)

class ReportProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report_Problem
        fields = ('__all__')
        
#revisar todos a baixo
class ProductLinkSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ['long_url']