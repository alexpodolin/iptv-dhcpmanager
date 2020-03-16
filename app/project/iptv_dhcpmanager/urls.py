from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('subnets/', views.subnets, name='subnets'),
    path('hosts-allow/', views.hosts_allow, name='hosts_allow'),
    path('auth/', views.auth, name='auth'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
]
