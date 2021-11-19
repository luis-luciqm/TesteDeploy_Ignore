from rest_framework import generics
from .serializers import GroupWhatsSerializer, MarginSerializer, MarginSerializerList, MessageSerializer
from groupswhats.models import *
from pechinchou_web.permissions import IsUserAdmin

class GroupsWhatsViewSet(generics.ListCreateAPIView):
    permission_classes = (IsUserAdmin,)
    serializer_class = GroupWhatsSerializer
    def get_queryset(self):
        queryset = GroupWhatsapp.objects.all()
        return queryset
        
    
class GroupsWhatsActiveListViewSet(generics.ListAPIView):
    permission_classes = (IsUserAdmin,)
    serializer_class = GroupWhatsSerializer
    def get_queryset(self):
        queryset = GroupWhatsapp.objects.filter(is_active = True)
        return queryset
            

class GroupWhatsEditViewSet(generics.UpdateAPIView):
    permission_classes = (IsUserAdmin,)
    serializer_class = GroupWhatsSerializer
    
    def get_queryset(self):
        queryset = GroupWhatsapp.objects.all()
        return queryset

class GroupWhatsDeleteViewSet(generics.DestroyAPIView):
    permission_classes = (IsUserAdmin,)
    serializer_class = GroupWhatsSerializer
    
    def get_queryset(self):
        queryset = GroupWhatsapp.objects.all()
        return queryset
    
class MarginListViewSet(generics.ListAPIView):
    serializer_class = MarginSerializerList
    def get_queryset(self):
        queryset = Margin.objects.all()
        return queryset
class MarginCreateViewSet(generics.CreateAPIView):
    permission_classes = (IsUserAdmin,)
    serializer_class = MarginSerializer

class MarginEditViewSet(generics.UpdateAPIView):
    permission_classes = (IsUserAdmin,)
    serializer_class = MarginSerializer
    queryset = Margin.objects.all()
    lookup_field = 'slug'
    
    
class MessageCreateViewSet(generics.CreateAPIView):
    permission_classes = (IsUserAdmin,)
    serializer_class = MessageSerializer
    
class MessageListViewSet(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    


    


    