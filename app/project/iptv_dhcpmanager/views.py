from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Subnets, Hosts_Allow

import ldap3
import io
import csv

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
		paginator = Paginator(hosts_allow, 15)

		page = request.GET.get('page')
		try:
			hosts_allow = paginator.page(page)
		except PageNotAnInteger:
			# Если страница не является целым числом, покажем 1-ю страницу.
			hosts_allow = paginator.page(1)
		except EmptyPage:
			# Если страница выходит за пределы диапазона (напр. 9999), покажем последнюю страницу.
			hosts_allow = paginator.page(paginator.num_pages)

		hosts_allow_count = Hosts_Allow.objects.count()

		template = loader.get_template('iptv_dhcpmanager/hosts_allow.html')
		context = {
			'hosts_allow': hosts_allow,
			'paginator': paginator,
			'hosts_allow_count': hosts_allow_count,
		}
		return HttpResponse(template.render(context, request))
		#return render(request,'iptv_dhcpmanager/hosts_allow.html', context)

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
		else:
			errors.append('Некорректный логин или пароль')
			return render(request, 'iptv_dhcpmanager/login.html', {'errors': errors})

def logout(request):
    '''Выход пользователя'''
    try:
        del request.session['login']
    except:
        pass
    return index(request)


def hadle_csv_file(file):
	'''Парсинг csv файла'''	

	for row in file:		
		row = row.decode(encoding='utf-8', errors='strict')
		row = row.split(';')
		#if row[0] != 'hostname':
		_, h_allow = Hosts_Allow.objects.update_or_create(
		hostname = row[0],
		mac_addr = row[1],
		ip_addr = row[2],
		description = row[3]
		)

	##data = csv.reader(open(file), delimiter=';')
	# for row in file:
	# 	if row[0] != 'hostname':			
	# 		h_allow = Hosts_Allow()
	# 		h_allow.hostname = str(row[0])
	# 		h_allow.mac_addr =  row[1]
	# 		h_allow.ip_addr = row[2]
	# 		h_allow.description = row[3]
	# 		h_allow.save()

def upload_csv(request):
	'''Сохранение загруженного файла'''
	if request.method == 'POST' and request.FILES['csv_file']:
		csv_file = request.FILES['csv_file']
		#fs = FileSystemStorage()
		#filename = fs.save(csv_file.name, csv_file)
		#uploaded_file_url = fs.url(filename)
		hadle_csv_file(csv_file)
		#return render(request, 'admin/iptv_dhcpmanager/hosts_allow/change_list.html', {'uploaded_file_url': uploaded_file_url})
		return redirect('/admin/iptv_dhcpmanager/hosts_allow/')
	#return render(request, 'admin/iptv_dhcpmanager/hosts_allow/change_list.html')
	return redirect('/admin/iptv_dhcpmanager/hosts_allow/')
