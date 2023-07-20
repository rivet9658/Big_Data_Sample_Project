# package
from django.db import models
from django.utils import timezone
# models
from base_app.models import BaseModel
from emoji.models import EmojiModel
from media.models import MediaModel
from tag.models import TagModel


class ArticleModel(BaseModel):
    title = models.CharField(max_length=150, verbose_name='文章標題')
    introduction = models.TextField(default='', verbose_name='文章簡介')
    is_publish = models.BooleanField(default=True, verbose_name='是否發佈')
    publish_datetime = models.DateTimeField(default=timezone.now, verbose_name='發佈日期')
    have_emoji = models.ManyToManyField(
        EmojiModel, through='ArticleHaveEmojiModel', through_fields=('belong_article', 'belong_emoji'),
        related_name='article_have_emoji', verbose_name='文章所含有之表情'
    )
    have_media = models.ManyToManyField(
        MediaModel, through='ArticleHaveMediaModel', through_fields=('belong_article', 'belong_media'),
        related_name='article_have_media', verbose_name='文章所含有之媒體(哪些媒體引用此文章)'
    )
    have_tag = models.ManyToManyField(
        TagModel, through='ArticleHaveTagModel', through_fields=('belong_article', 'belong_tag'),
        related_name='article_have_tag', verbose_name='文章所含有之標籤'
    )

    class Meta:
        db_table = "article"


# 圖片存放路徑
def article_image_path(instance, filename):
    belong_order = instance.order
    belong_article = instance.belong_article.id

    return f"static/images/article/{str(belong_article)}/{belong_order}/{filename}"


class ArticleHaveImageModel(BaseModel):
    order = models.IntegerField(default=0, verbose_name='所屬段落順序(0為標題圖片)')
    image = models.ImageField(upload_to=article_image_path, verbose_name='圖片檔案')
    name = models.CharField(default='', max_length=50, verbose_name='圖片名稱(檔案名稱)')
    source = models.TextField(default='', verbose_name='圖片來源(檔案來源)')
    belong_article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE,
                                       related_name='article_have_image', verbose_name='所屬文章')

    class Meta:
        db_table = "article_have_image"


class ArticleHaveEmojiModel(BaseModel):
    belong_article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE,
                                       related_name='article_have_emoji_article', verbose_name='所屬文章')
    belong_emoji = models.ForeignKey(EmojiModel, on_delete=models.CASCADE,
                                     related_name='article_have_emoji_emoji', verbose_name='所屬表情')

    class Meta:
        db_table = "article_have_emoji"


class ArticleHaveMediaModel(BaseModel):
    report_url = models.TextField(default='', verbose_name='媒體引用連結')
    belong_article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE,
                                       related_name='article_have_media_article', verbose_name='所屬文章')
    belong_media = models.ForeignKey(MediaModel, on_delete=models.CASCADE,
                                     related_name='article_have_media_media', verbose_name='所屬媒體')

    class Meta:
        db_table = "article_have_media"


class ArticleHaveTagModel(BaseModel):
    belong_article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE,
                                       related_name='article_have_tag_article', verbose_name='所屬文章')
    belong_tag = models.ForeignKey(TagModel, on_delete=models.CASCADE,
                                   related_name='article_have_tag_tag', verbose_name='所屬標籤')

    class Meta:
        db_table = "article_have_tag"
