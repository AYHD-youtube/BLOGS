from this import s
from urllib import response
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from blogs.serializers import BlogsSerializer, UserSerializer
from .models import Blogs
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import *
from django.http import JsonResponse


class UserCreate(APIView):
    """ 
    Creates the user. 
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = User.objects.create(username=serializer.data['email'], email=serializer.data['email'])
            user.set_password(request.data['password'])
            user.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return JsonResponse(data=json, status=201)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    """ 
    Login the user. 
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, format='json'):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            token = Token.objects.get(user=user)
            json = UserSerializer(user).data
            json['token'] = token.key
            return JsonResponse(json, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((AllowAny,))
def blogs_list(request):
    """
    List all blogs
    """
    if request.method == 'GET':
        blogs = Blogs.objects.all()
        serializer = BlogsSerializer(blogs, many=True)
        return JsonResponse(serializer.data)

# add blog if user is logged in
@api_view(['POST'])
@permission_classes((AllowAny,))
def blogs_add(request):
    """
    Add a blog
    """
    if not request.data['token']:
        return JsonResponse({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        token = Token.objects.get(key=request.data['token'])
        user = token.user

        if not user:
            return JsonResponse({'error': 'User is missing'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['author'] = user
        request.data['is_published'] = True if request.data['publish'] == 'true' else False
        serializer = BlogsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# home page render
def home(request):
    blogs = Blogs.objects.all()
    return render(request, 'home.html', {'blogs': blogs})

def create_blog(request):
    if request.COOKIES['token']:
        auth = Token.objects.get(key=request.COOKIES['token'])
        user = auth.user
        if user:
            return render(request, 'create_blog.html')
    return redirect('/login_or_register')

def login_or_register(request):
    return render(request, 'login_or_register.html')