from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('subnets/', views.subnets, name='subnets'),
    path('hosts-allow/', views.hosts_allow, name='hosts_allow'),
    path('auth/', views.auth, name='auth'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('generate_subnets/', views.generate_subnets, name='generate_subnets'),
    path('generate_allowed_hosts/', views.generate_allowed_hosts, name='generate_allowed_hosts'),
    path('search_host/', views.SearchHostResultsView.as_view(), name='search_host'),    
]
