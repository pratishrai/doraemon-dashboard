from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('user/', views.user, name='user'),
    path('logout/', views.user, name='logout')
]
