from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('user/', views.user, name='user'),
    path('commands/', views.commands, name='cmds'),
    path('docs/', views.docs, name='docs'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
