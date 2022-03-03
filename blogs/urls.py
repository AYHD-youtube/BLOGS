from django.urls import path
from blogs import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/register', views.UserCreate.as_view(), name='api_register'),
    path('api/login', views.UserLogin.as_view(), name='api_login'),
    path('api/blogs_list', views.blogs_list, name='api_blogs_list'),
    path('api/blogs_add', views.blogs_add, name='api_blogs_add'),
    path('create_blog', views.create_blog, name='create_blog'),
    path('login_or_register', views.login_or_register, name='login_or_register'),
]