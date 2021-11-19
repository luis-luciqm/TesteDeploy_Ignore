from rest_framework import serializers
from groupswhats.models import *

class GroupWhatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupWhatsapp  
        fields = ('__all__')
        
class MarginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Margin  
        fields = ('name', 'init', 'finish')

class MarginSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Margin  
        fields = ('__all__')
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('__all__')
    
        