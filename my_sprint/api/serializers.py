from rest_framework import serializers
from .models import User, Coords, PerevalAdded

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']

class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()

    class Meta:
        model = PerevalAdded
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level_winter', 'level_summer', 'level_autumn', 'level_spring', 'status']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        user = User.objects.create(**user_data)
        coords = Coords.objects.create(**coords_data)
        pereval_added = PerevalAdded.objects.create(user=user, coords=coords, **validated_data)
        return pereval_added

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        coords_data = validated_data.pop('coords', None)
        
        if user_data:
            User.objects.filter(id=instance.user.id).update(**user_data)
        if coords_data:
            Coords.objects.filter(id=instance.coords.id).update(**coords_data)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
