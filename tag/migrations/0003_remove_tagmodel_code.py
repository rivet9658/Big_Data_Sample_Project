# Generated by Django 3.2.20 on 2023-07-17 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_auto_20230716_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagmodel',
            name='code',
        ),
    ]
