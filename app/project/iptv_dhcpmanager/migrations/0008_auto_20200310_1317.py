# Generated by Django 3.0.3 on 2020-03-10 10:17

from django.db import migrations, models
import macaddress.fields


class Migration(migrations.Migration):

    dependencies = [
        ('iptv_dhcpmanager', '0007_auto_20200228_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hosts_allow',
            name='mac_addr',
            field=macaddress.fields.MACAddressField(integer=True, max_length=17, verbose_name='mac адрес'),
        ),
        migrations.AlterField(
            model_name='subnets',
            name='gw_subnet',
            field=models.GenericIPAddressField(protocol='IPv4', verbose_name='ip шлюза'),
        ),
        migrations.AlterField(
            model_name='subnets',
            name='ip_subnet',
            field=models.GenericIPAddressField(protocol='IPv4', verbose_name='ip подсети'),
        ),
        migrations.AlterField(
            model_name='subnets',
            name='mask_subnet',
            field=models.GenericIPAddressField(protocol='IPv4', verbose_name='Маска Подсети'),
        ),
    ]
