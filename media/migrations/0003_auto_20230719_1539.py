# Generated by Django 3.2.20 on 2023-07-19 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20230716_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediamodel',
            name='image_name',
            field=models.CharField(default='', max_length=50, verbose_name='媒體圖片名稱(檔案名稱)'),
        ),
        migrations.AddField(
            model_name='mediamodel',
            name='image_source',
            field=models.URLField(default='', max_length=150, verbose_name='媒體圖片來源(檔案來源)'),
        ),
    ]