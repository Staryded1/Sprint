from rest_framework import serializers

class PassSerializer(serializers.Serializer):
    column1 = serializers.CharField(max_length=100)
    column2 = serializers.CharField(max_length=100)