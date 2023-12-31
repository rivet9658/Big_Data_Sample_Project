# Generated by Django 3.2.20 on 2023-07-15 15:19

import base_app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0002_auto_20230715_2319'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='資料創建時間')),
                ('updated_datetime', models.DateTimeField(auto_now=True, verbose_name='資料最後更新時間')),
                ('content', models.TextField(default='', verbose_name='留言內容')),
                ('belong_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_belong_article', to='article.articlemodel', verbose_name='留言對應之文章')),
                ('create_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='commentmodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者')),
                ('updated_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='commentmodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
    ]
