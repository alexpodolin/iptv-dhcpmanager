from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView
from django.db.models import Q 

from .models import Subnets, Hosts_Allow

import ldap3
import os
import csv
import shutil
import subprocess

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
		_, h_allow = Hosts_Allow.objects.update_or_create(
		hostname = row[0],
		mac_addr = row[1],
		ip_addr = row[2],
		description = row[3]
		)

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

conf_dir = '/etc/dhcp/'

def restart_dhcpd(conf_path, conf_path_bkp):
	'''Перезапуск серввиса'''
	cmd = '/usr/bin/systemctl restart dhcpd'
	retcode = subprocess.call(cmd, shell=True)
	if retcode == 0:
		os.remove(conf_path_bkp)
	else:
		shutil.copy2(conf_path_bkp, conf_path)
		subprocess.call(cmd, shell=True)
		os.remove(conf_path_bkp)

def generate_subnets(request):
	'''Гененрация файла с конфигурацией подсети'''
	conf_path = os.path.join(conf_dir, 'subnets.conf')
	conf_path_bkp = os.path.join(conf_dir, 'subnets.conf.bkp')
	shutil.copy2(conf_path, conf_path_bkp)

	subnets_list = Subnets.objects.all()

	with open(conf_path, 'w+') as result:
		for item in subnets_list:
			result.write('# ' + item.description + '\n')
			result.write('subnet ' + item.ip_subnet + \
						' netmask ' + item.mask_subnet + ' {' + '\n')
			result.write('  option routers\t\t' + item.gw_subnet + ';' +'\n')
			result.write('  option subnet-mask\t\t' + item.mask_subnet + ';' +'\n')
			result.write('  option broadcast-address\t' + item.ip_broadcast + ';' +'\n')
			result.write('  option domain-name\t\t"' + item.dns_prefix +'"' + ';' +'\n')
			if item.dns_res == None:
<<<<<<< HEAD
			    item.dns_res = ''
			    result.write('  option domain-name-servers\t' + item.dns_main + item.dns_res + ';' +'\n'*2)
			else:
			     result.write('  option domain-name-servers\t' + item.dns_main + ', ' + item.dns_res + ';' +'\n'*2)
=======
				item.dns_res = ''
			result.write('  option domain-name-servers\t' + item.dns_main + item.dns_res + ';' +'\n'*2)
>>>>>>> c9ea7f663d31032ec8e4e88866935b1c29f78819
			result.write('  pool {' + '\n')
			result.write('    deny\tunknown-clients;' + '\n')
			result.write('    range\t' + item.ip_start + ' ' + item.ip_end + ';' +'\n')
			result.write('  }' + '\n')
			result.write('}' + '\n'*2)
	restart_dhcpd(conf_path, conf_path_bkp)	
	return redirect('/admin/iptv_dhcpmanager/subnets/')

def generate_allowed_hosts(request):	
	'''Гененрация файла с конфигурацией хоста'''
	conf_path = os.path.join(conf_dir, 'hosts_allow.conf')
	conf_path_bkp = os.path.join(conf_dir, 'hosts_allow.conf.bkp')
	shutil.copy2(conf_path, conf_path_bkp)

	hosts_allow = Hosts_Allow.objects.all()

	with open(conf_path, 'w+') as result:
		for item in hosts_allow:
			result.write('host ' + str(item.hostname) + \
				' { hardware ethernet ' + str(item.mac_addr) + ';' \
				' fixed-address ' + str(item.ip_addr) + '; }' + '\n')
	restart_dhcpd(conf_path, conf_path_bkp)	
	return redirect('/admin/iptv_dhcpmanager/hosts_allow/')

class SearchHostResultsView(ListView):
	model = Hosts_Allow
	template_name = 'iptv_dhcpmanager/search_host_results.html'

	def get_queryset(self):
		query = self.request.GET.get('q')
		object_list =  Hosts_Allow.objects.filter(
			Q(hostname__icontains=query) |
			Q(mac_addr__icontains=query) |
			Q(ip_addr__icontains=query) |
			Q(description__icontains=query)
		)

		return object_list

