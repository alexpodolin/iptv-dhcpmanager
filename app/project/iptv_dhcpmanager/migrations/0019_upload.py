# Generated by Django 3.0.3 on 2020-03-16 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv_dhcpmanager', '0018_delete_csv_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_obj', models.FileField(upload_to='media/')),
            ],
        ),
    ]