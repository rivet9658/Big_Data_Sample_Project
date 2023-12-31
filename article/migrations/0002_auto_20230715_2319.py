# Generated by Django 3.2.20 on 2023-07-15 15:19

import article.models
import base_app.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        ('emoji', '0001_initial'),
        ('media', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='introduction',
            field=models.TextField(default='', verbose_name='文章簡介'),
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 15, 23, 19, 20, 340004), verbose_name='時間戳記(要顯示的日期時間)'),
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='title',
            field=models.CharField(max_length=50, verbose_name='文章標題'),
        ),
        migrations.CreateModel(
            name='ArticleHaveTagModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='資料創建時間')),
                ('updated_datetime', models.DateTimeField(auto_now=True, verbose_name='資料最後更新時間')),
                ('belong_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_have_tag_article', to='article.articlemodel', verbose_name='所屬文章')),
                ('belong_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_have_tag_tag', to='tag.tagmodel', verbose_name='所屬標籤')),
                ('create_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehavetagmodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者')),
                ('updated_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehavetagmodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者')),
            ],
            options={
                'db_table': 'article_have_tag',
            },
        ),
        migrations.CreateModel(
            name='ArticleHaveMediaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='資料創建時間')),
                ('updated_datetime', models.DateTimeField(auto_now=True, verbose_name='資料最後更新時間')),
                ('belong_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_have_media_article', to='article.articlemodel', verbose_name='所屬文章')),
                ('belong_media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_have_media_media', to='media.mediamodel', verbose_name='所屬媒體')),
                ('create_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehavemediamodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者')),
                ('updated_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehavemediamodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者')),
            ],
            options={
                'db_table': 'article_have_media',
            },
        ),
        migrations.CreateModel(
            name='ArticleHaveImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='資料創建時間')),
                ('updated_datetime', models.DateTimeField(auto_now=True, verbose_name='資料最後更新時間')),
                ('order', models.IntegerField(default=0, verbose_name='所屬段落順序(0為標題圖片)')),
                ('name', models.CharField(default='', max_length=50, verbose_name='圖片名稱(檔案名稱)')),
                ('source', models.URLField(default='', max_length=150, verbose_name='圖片來源(檔案來源)')),
                ('image', models.ImageField(upload_to=article.models.article_image_path, verbose_name='圖片檔案')),
                ('belong_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_have_image', to='article.articlemodel', verbose_name='所屬文章')),
                ('create_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehaveimagemodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者')),
                ('updated_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehaveimagemodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleHaveEmojiModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='資料創建時間')),
                ('updated_datetime', models.DateTimeField(auto_now=True, verbose_name='資料最後更新時間')),
                ('belong_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_have_emoji_article', to='article.articlemodel', verbose_name='所屬文章')),
                ('belong_emoji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_have_emoji_emoji', to='emoji.emojimodel', verbose_name='所屬表情')),
                ('create_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehaveemojimodel_create_user', to=settings.AUTH_USER_MODEL, verbose_name='資料創建者')),
                ('updated_user', models.OneToOneField(on_delete=models.SET(base_app.models.get_anonymous_user), related_name='articlehaveemojimodel_updated_user', to=settings.AUTH_USER_MODEL, verbose_name='資料最後更新者')),
            ],
            options={
                'db_table': 'article_have_emoji',
            },
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='have_emoji',
            field=models.ManyToManyField(related_name='article_have_emoji', through='article.ArticleHaveEmojiModel', to='emoji.EmojiModel', verbose_name='文章所含有之表情'),
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='have_media',
            field=models.ManyToManyField(related_name='article_have_media', through='article.ArticleHaveMediaModel', to='media.MediaModel', verbose_name='文章所含有之媒體(哪些媒體引用此文章)'),
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='have_tag',
            field=models.ManyToManyField(related_name='article_have_tag', through='article.ArticleHaveTagModel', to='tag.TagModel', verbose_name='文章所含有之標籤'),
        ),
    ]
