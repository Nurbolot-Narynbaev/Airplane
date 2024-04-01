from rest_framework import serializers
from django.db.models import Avg


from .models import (
    Producer,
    Airplane,
    Type
    )

from apps.review.serializers import CommentSerializer, LikeSerializer

class ProducerCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 1

    class Meta:
        model = Producer
        exclude = ('slug',)

    def validate(self, attrs):
        producer = attrs.get('title')
        if Producer.objects.filter(title=producer).exists():
            raise serializers.ValidationError(
                'This producer already exists'
            )
        user = self.context['request'].user                   # 1
        attrs['user'] = user
        return attrs
    

class ProducerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer 
        fields = ['title', 'slug', 'user']  # 2


class ProducerRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 3

    class Meta:
        model = Producer
        fields = '__all__'

    def validate(self, attrs):                               # 3
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class AirplaneCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') # 4
    
    class Meta:
        model = Airplane
        exclude = ('slug',)

    def validate(self, attrs: dict):
        airplane = attrs.get('title')
        if Airplane.objects.filter(title=airplane).exists():
            raise serializers.ValidationError(
                'This Airplane already exists'
            )
        user = self.context['request'].user                 # 4
        attrs['user'] = user
        return attrs
    

class AirplaneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane  
        fields = ['title', 'producer', 'slug', 'user']       # 5


class AirplaneUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 6

    class Meta:
        model = Airplane                                          # 6
        fields = ['title', 'producer', 'desc', 'image', 'year_publ', 'slug', 'status', 'airplane', 'type', 'user']
    
    def validate(self, attrs):                                 # 6
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class AirplaneRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   # 7

    class Meta:
        model = Airplane
        fields = '__all__'

    def validate(self, attrs):                                 # 7
        user = self.context['request'].user
        attrs['user'] = user
        return attrs
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['comments'] = CommentSerializer(
        instance.airplanes_comments.all(), many=True
        ).data

        rating = instance.airplanes_ratings.aggregate(Avg('rating'))['rating__avg']   
        if rating:
            rep['rating'] = round(rating, 1) 
        else:
            rep['rating'] = 0.0
        
        rep['likes'] = instance.airplanes_likes.all().count()
        rep['liked_by'] = LikeSerializer(
            instance.airplanes_likes.all().only('user'), many=True).data 

        return rep


class TypeCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   # 8

    class Meta:
        model = Type
        fields = ['type', 'user']                             # 8

    def validate(self, attrs):
        type = attrs.get('type')
        if Type.objects.filter(type=type).exists():
            raise serializers.ValidationError(
                'Such type already exists'
            )
        user = self.context['request'].user                    # 8
        attrs['user'] = user
        return attrs


class TypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class TypeRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    # 9
    airplanes = AirplaneListSerializer(read_only=True, many=True)

    class Meta: 
        model = Type  
        fields ="__all__"                    # 9

    def to_representation(self, instance: Type):
        airplanes = instance.airplane_type.all()
        rep = super().to_representation(instance)
        rep['airplanes'] = AirplaneListSerializer(
            instance=airplanes, many=True).data
        return rep
    
    def validate(self, attrs):                                   # 9
        user = self.context['request'].user
        attrs['user'] = user
        return attrs