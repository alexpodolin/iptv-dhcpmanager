from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('subnets/', views.subnets, name='subnets'),
    path('hosts-allow/', views.hosts_allow, name='hosts_allow'),
    path('auth/', views.auth, name='hosts_allow'),

]
