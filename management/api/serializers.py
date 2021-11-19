from django.db.models.base import Model
from rest_framework import serializers
from management.models import *


        
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('__all__')

class CategorySerializer(serializers.ModelSerializer):

    subcategory = SubcategorySerializer(source='subcategorys',many=True)
    class Meta:
        model = Category
        fields = ('__all__')

#revisar   
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('__all__')    