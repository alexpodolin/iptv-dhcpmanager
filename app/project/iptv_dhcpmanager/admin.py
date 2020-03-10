from django.contrib import admin
from .models import Subnets, Hosts_Allow
import shutil
import subprocess
import os

conf_dir = '/tmp'

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

class AdminSubnet(admin.ModelAdmin):
	list_display = ('description', 'ip_subnet', 'mask_subnet', 'gw_subnet', \
					'ip_broadcast', 'ip_start', 'ip_end', 'dns_prefix', 'dns_main', 'dns_res' )
	actions = ['genSubnet']
	
	def genSubnet(ModelAdmin, request, queryset):
		'''Гененрация файла с конфигурацией подсети'''
		conf_path = os.path.join(conf_dir, 'subnets.conf')
		conf_path_bkp = os.path.join(conf_dir, 'subnets.conf.bkp')
		shutil.copy2(conf_path, conf_path_bkp)

		with open('/tmp/subnets.conf', 'w+') as result:
			for item in queryset:
				result.write('# ' + item.description + '\n')
				result.write('subnet ' + item.ip_subnet + \
							' netmask ' + item.mask_subnet + ' {' + '\n')
				result.write('  option routers\t\t' + item.gw_subnet + ';' +'\n')
				result.write('  option subnet-mask\t\t' + item.ip_subnet + ';' +'\n')
				result.write('  option broadcast-address\t' + item.ip_broadcast + ';' +'\n')
				result.write('  option domain-name\t\t"' + item.dns_prefix +'"' + ';' +'\n')
				if item.dns_res == None:
					item.dns_res = ''
				result.write('  option domain-name-servers\t' + item.dns_main + item.dns_res + ';' +'\n'*2)
				result.write('  pool {' + '\n')
				result.write('    deny\tunknown-clients;' + '\n')
				result.write('    range\t' + item.ip_start + ' ' + item.ip_end + '\n')
				result.write('  }' + '\n')
				result.write('}' + '\n'*2)
		restart_dhcpd(conf_path, conf_path_bkp)	

	genSubnet.short_description = 'Создать конфиг подсетей'
	

class AdminHosts_Allow(admin.ModelAdmin):
	list_display = ('hostname', 'mac_addr', 'ip_addr', 'description')
	actions = ['genHostAllow']
	
	def genHostAllow(ModelAdmin, request, queryset):
		'''Гененрация файла с конфигурацией хоста'''
		conf_path = os.path.join(conf_dir, 'hosts_allow.conf')
		conf_path_bkp = os.path.join(conf_dir, 'hosts_allow.conf.bkp')
		shutil.copy2(conf_path, conf_path_bkp)

		with open('/tmp/hosts_allow.conf', 'w+') as result:
			for item in queryset:
				result.write('host ' + item.hostname + \
					' { hardware ethernet ' + item.mac_addr + ';' \
					' fixed-address ' + item.ip_addr + '; }' + '\n')
		restart_dhcpd(conf_path, conf_path_bkp)	

	genHostAllow.short_description = 'Создать список доступных хостов'

admin.site.register(Subnets, AdminSubnet)
admin.site.register(Hosts_Allow, AdminHosts_Allow)


