# Generated by Django 3.2.20 on 2023-07-17 06:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20230716_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodel',
            name='leave_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='留言日期'),
        ),
    ]