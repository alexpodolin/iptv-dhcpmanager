from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Subnets, Hosts_Allow
import ldap3

def index(request):
	'''Стартовая страница'''
	return render(request, 'iptv_dhcpmanager/login.html')

def login(request):
	'''Вход в систему'''
	return render(request,'iptv_dhcpmanager/login.html')

def subnets(request):
	'''Просмотр доступных подсетей'''
	subnets_list = Subnets.objects.all()
	template = loader.get_template('iptv_dhcpmanager/subnets.html')
	context = {
        'subnets_list': subnets_list,
    }
	return HttpResponse(template.render(context, request))

def hosts_allow(request):
	'''Просмотр список зарезервированных ip адресов'''
	hosts_allow = Hosts_Allow.objects.all()
	template = loader.get_template('iptv_dhcpmanager/hosts_allow.html')
	context = {
		'hosts_allow': hosts_allow
	}
	return HttpResponse(template.render(context, request))

def checkConnLDAP(username, password):
	'''Соединимся с LDAP'''
	server = ldap3.Server('sats.local')
	user = 'sats\\' + username
	passwd = password
	conn = ldap3.Connection(server, user, passwd)
	conn = conn.bind()
	return conn

def auth(request):
	'''Аутентификация пользователя'''
	errors = []
	if request.method == 'POST':
		login = request.POST['form-login']
		password = request.POST['form-passwd']

		if checkConnLDAP(login, password):
			return subnets(request)
		else:
			errors.append('Некорректный логин или пароль')
			return render(request, 'iptv_dhcpmanager/login.html', {'errors': errors})