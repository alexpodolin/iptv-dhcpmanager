from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

import ldap3

def index(request):
	'''Стартовая страница'''
	return render(request, 'iptv_dhcpmanager/login.html')

def login(request):
	'''Вход в систему'''
	return render(request,'iptv_dhcpmanager/login.html')

def subnets(request):
	'''Просмотр доступных подсетей'''
	return render(request,'iptv_dhcpmanager/subnets.html')

def hosts_allow(request):
	'''Просмотр список зарезервированных ip адресов'''
	return render(request,'iptv_dhcpmanager/hosts_allow.html')

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
#			return render(request, 'iptv_dhcpmanager/subnets.html')
			return subnets(request)
		else:
			errors.append('Некорректный логин или пароль')
			return render(request, 'iptv_dhcpmanager/login.html', {'errors': errors})