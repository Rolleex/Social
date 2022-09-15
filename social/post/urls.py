from django.urls import path
from .views import *

urlpatterns = [
    path('News/', viewpost, name='viewpost'),
    path('liked/<pk>', like, name='liked'),
    path('unliked/<pk>', unlike, name='unliked'),

]
