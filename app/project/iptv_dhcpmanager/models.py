from django.db import models

# Create your models here.

class Subnets(models.Model):
	description = models.CharField(max_length=150)
	ip_subnet = models.GenericIPAddressField(protocol='IPv4', blank=False)
	mask_subnet = models.GenericIPAddressField(protocol='IPv4', blank=False)
	gw_subnet = models.GenericIPAddressField(protocol='IPv4', blank=False)
	ip_start = models.GenericIPAddressField(protocol='IPv4', blank=False)
	ip_end = models.GenericIPAddressField(protocol='IPv4', blank=False)
	ip_broadcast = models.GenericIPAddressField(protocol='IPv4', blank=False)
	dns_prefix = models.CharField(max_length=30, default='eltex.local')
	dns_main = models.GenericIPAddressField(protocol='IPv4', default='10.22.0.3', blank=False)
	dns_res = models.GenericIPAddressField(protocol='IPv4', default='')

	def __str__(self):
		return '{}'.format(self.title)

class Hosts_Allow(models.Model):
	hostname = models.CharField(max_length=30, blank=False)
	mac_addr = models.CharField(max_length=17, blank=False)
	ip_addr = models.GenericIPAddressField(protocol='IPv4', blank=False)
	description = models.CharField(max_length=150)

	def __str__(self):
		return '{}'.format(self.title)
		

		