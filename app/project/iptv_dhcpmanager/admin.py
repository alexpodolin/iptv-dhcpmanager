from django.contrib import admin

from .models import Subnets, Hosts_Allow

class AdminSubnet(admin.ModelAdmin):
	list_display = ('description', 'ip_subnet', 'mask_subnet', 'gw_subnet', \
					'ip_broadcast', 'ip_start', 'ip_end', 'dns_prefix', 'dns_main', 'dns_res' )

	actions = ['genSubnet']
	def genSubnet(ModelAdmin, request, queryset):
		#queryset.objects.all()
		pass
	genSubnet.short_description = 'Создать конфиг подсетей'

class AdminHosts_Allow(admin.ModelAdmin):
	list_display = ('hostname', 'mac_addr', 'ip_addr', 'description')

	actions = ['genHostAllow']
	def genHostAllow(ModelAdmin, request, queryset):
		with open('/tmp/res.txt', 'w+') as result:
			for item in queryset:
				result.write('host ' + item.hostname + ' { hardware ethernet ' + item.mac_addr + ';' \
							 ' fixed-address ' + item.ip_addr + '; }' + '\n')

	genHostAllow.short_description = 'Создать список доступных хостов'
		

admin.site.register(Subnets, AdminSubnet)
admin.site.register(Hosts_Allow, AdminHosts_Allow)


