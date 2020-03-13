from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from .models import Subnets, Hosts_Allow

import ldap3
import csv
import io

def index(request):
	'''Стартовая страница'''
	return render(request, 'iptv_dhcpmanager/login.html')

def subnets(request):
	'''Просмотр доступных подсетей'''
	if not request.session.get('login'):
		return redirect('/')
	else:
		subnets_list = Subnets.objects.all()
		template = loader.get_template('iptv_dhcpmanager/subnets.html')
		context = {
        	'subnets_list': subnets_list,
    	}
		return HttpResponse(template.render(context, request))

def hosts_allow(request):
	'''Просмотр список зарезервированных ip адресов'''
	if not request.session.get('login'):
		return redirect('/')
	else:
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
			request.session['login'] = login
			request.session.set_expiry(300)
			return redirect('/subnets/')
			#return subnets(request)
		else:
			errors.append('Некорректный логин или пароль')
			return render(request, 'iptv_dhcpmanager/login.html', {'errors': errors})

def logout(request):
    '''Выход пользователя'''
    try:
        del request.session['username']
    except:
        pass
    return index(request)


#def handle_upload_file(file):


def upload_csv(request):
	'''массовая загрузка hosts allow из csv'''
	return render(request)

