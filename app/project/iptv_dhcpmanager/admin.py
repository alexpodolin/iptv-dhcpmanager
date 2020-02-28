from django.contrib import admin

# Register your models here.

from .models import Subnets, Hosts_Allow

class AdminSubnet(admin.ModelAdmin):
	list_display = ('description', 'ip_subnet', 'mask_subnet', 'gw_subnet', \
					'ip_broadcast', 'ip_start', 'ip_end', 'dns_prefix', 'dns_main', 'dns_res' )

class AdminHosts_Allow(admin.ModelAdmin):
	list_display = ('hostname', 'mac_addr', 'ip_addr', 'description')

admin.site.register(Subnets, AdminSubnet)
admin.site.register(Hosts_Allow, AdminHosts_Allow)


