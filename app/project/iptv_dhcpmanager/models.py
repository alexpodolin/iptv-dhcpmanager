from macaddress.fields import MACAddressField

from django.db import models

class Subnets(models.Model):
	class Meta:
		verbose_name = '\"Подсеть\"'
		verbose_name_plural = 'Подсети'

	description = models.CharField(max_length=100, verbose_name='Описание')
	ip_subnet = models.GenericIPAddressField(protocol='IPv4', blank=False, verbose_name='ip подсети')
	mask_subnet = models.GenericIPAddressField(protocol='IPv4', blank=False, verbose_name='Маска Подсети')
	gw_subnet = models.GenericIPAddressField(protocol='IPv4', blank=False, verbose_name='ip шлюза')	
	ip_broadcast = models.GenericIPAddressField(protocol='IPv4', blank=False, verbose_name='Широковещательный адрес')
	ip_start = models.GenericIPAddressField(protocol='IPv4', blank=False, verbose_name='ip начальный')
	ip_end = models.GenericIPAddressField(protocol='IPv4', blank=False, verbose_name='ip конечный')
	dns_prefix = models.CharField(max_length=30, default='eltex.local', verbose_name='dns префикс')
	dns_main = models.GenericIPAddressField(protocol='IPv4', default='10.22.0.3', blank=False, verbose_name='Осн. dns сервер')
	dns_res = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True, verbose_name='Резерв. dns сервер')

class Hosts_Allow(models.Model):
	class Meta:
		verbose_name = '\"Доступные/Зарезервированные ip\"'
		verbose_name_plural = 'Доступные/Зарезервированные ip'

	hostname = models.CharField(max_length=30, blank=False, verbose_name='Имя хоста')
	#mac_addr = models.CharField(max_length=17, blank=False, verbose_name='mac адрес')
	mac_addr = MACAddressField(max_length=17, blank=False, verbose_name='mac адрес')
	ip_addr = models.GenericIPAddressField(protocol='IPv4', blank=False, verbose_name='ip адрес')
	description = models.CharField(max_length=100, verbose_name='Описание')
