# Generated by Django 3.2.20 on 2023-07-16 11:32

import base_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='commentmodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='updated_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='commentmodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者'),
        ),
    ]
