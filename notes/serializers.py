from rest_framework import serializers
from .models import Notes, Category

class notesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'
        # fields = ('title', 'content', 'category', 'due_date', 'priority', 'created_time', 'user')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'