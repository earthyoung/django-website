from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *


app_name = 'bulletinapp'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('join/', JoinView.as_view(), name='join'),
    path('login/', LoginView.as_view(), name='login'),
    path('', MainView.as_view(), name='main'),
    path('my_page/', MyPageView.as_view(), name='my_page'),
    path('create/', CreateView.as_view(), name='create'),
    path('post/<int:post_id>/', ContentView.as_view(), name='post_content'),
    path('logout/', logout, name='logout'),
    path('my_page/my_post/', MyContentView.as_view(), name='my_post'),
    path('withdrawal/', account_withdrawal, name='withdrawal'),
    path('delete/<int:pk>/', post_delete, name='post_delete'),
    path('change_info/<str:data>/', ChangeInfoView.as_view(), name='change_info'),
    path('update/<int:pk>/', UpdateView.as_view(), name='update'),
]
