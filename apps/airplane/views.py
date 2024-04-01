from rest_framework.viewsets import ModelViewSet, GenericViewSet   
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)   

from .models import (
    Producer,
    Airplane,
    Type     
)
from .permissions import (
    IsOwner
)

from .serializers import (
    ProducerCreateSerializer, 
    ProducerListSerializer, 
    ProducerRetrieveSerializer,
    
    AirplaneCreateSerializer, 
    AirplaneListSerializer, 
    AirplaneUpdateSerializer, 
    AirplaneRetrieveSerializer,

    TypeCreateSerializer,   
    TypeListSerializer,     
    TypeRetrieveSerializer  
)

class ProducerViewSet(ModelViewSet):      
    queryset = Producer.objects.all()
    serializer_class = ProducerCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ProducerCreateSerializer
        elif self.action == 'list':
            return ProducerListSerializer
        elif self.action == 'retrieve':
            return ProducerRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    

class AirplaneViewSet(ModelViewSet):      # CRUD - Create, Retrieve, Update, Delete, 
    queryset = Airplane.objects.all()
    serializer_class = AirplaneCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AirplaneCreateSerializer
        elif self.action == 'list':
            return AirplaneListSerializer
        elif self.action in ['update', 'partial_update']:
            return AirplaneUpdateSerializer
        elif self.action == 'retrieve':
            return AirplaneRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        producer_id = request.query_params.get('producer_id')
        if producer_id:
            queryset = queryset.filter(producer_id=producer_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TypeViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TypeCreateSerializer
        elif self.action == 'list':
            return TypeListSerializer
        elif self.action == 'retrieve':
            return TypeRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()