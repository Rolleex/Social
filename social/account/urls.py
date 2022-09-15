from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('create_profile_page/', edit, name='edit'),
    path('profile/<str:slug>', ProfilePage.as_view(), name='profile'),
    path('follow/<username>', follow, name='follow'),
    path('unfollow/<username>', unfollow, name='unfollow'),
    path('logout', user_logout, name='logout'),
    path('search/', Search.as_view(), name='search'),
    path('user/<username>/', user, name='user'),

]
