from rest_framework import serializers
from blogs.models import Blogs
from django.contrib.auth.models import User

class BlogsSerializer(serializers.Serializer):
     class Meta:
        model = Blogs
        fields = ('id', 'title', 'content', 'author', 'created_at', 'updated_at', 'is_published')
        read_only_fields = ('id', 'created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
