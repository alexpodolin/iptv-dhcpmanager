# Generated by Django 3.0.3 on 2020-03-13 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv_dhcpmanager', '0008_auto_20200310_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='uploads/')),
            ],
        ),
    ]