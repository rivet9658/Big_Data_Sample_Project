# Generated by Django 3.2.20 on 2023-07-16 11:32

import base_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0004_alter_articlemodel_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlehaveemojimodel',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehaveemojimodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者'),
        ),
        migrations.AlterField(
            model_name='articlehaveemojimodel',
            name='updated_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehaveemojimodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者'),
        ),
        migrations.AlterField(
            model_name='articlehaveimagemodel',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehaveimagemodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者'),
        ),
        migrations.AlterField(
            model_name='articlehaveimagemodel',
            name='updated_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehaveimagemodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者'),
        ),
        migrations.AlterField(
            model_name='articlehavemediamodel',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehavemediamodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者'),
        ),
        migrations.AlterField(
            model_name='articlehavemediamodel',
            name='updated_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehavemediamodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者'),
        ),
        migrations.AlterField(
            model_name='articlehavetagmodel',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehavetagmodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者'),
        ),
        migrations.AlterField(
            model_name='articlehavetagmodel',
            name='updated_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehavetagmodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者'),
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlemodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者'),
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='updated_user',
            field=models.ForeignKey(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlemodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者'),
        ),
    ]
