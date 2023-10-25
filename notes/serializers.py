from rest_framework import serializers
from .models import Notes, Category

class notesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'