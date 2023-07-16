# package
from django.db import models
# models
from base_app.models import BaseModel
from article.models import ArticleModel


# 計算該筆段落是對應文章的第幾段
def now_order(instance):
    return ParagraphModel.objects.filter(belong_article=instance.belong_article).count() + 1


class ParagraphModel(BaseModel):
    title = models.CharField(max_length=50, verbose_name='段落標題')
    content = models.TextField(default='', verbose_name='段落內文')
    order = models.IntegerField(default=now_order, verbose_name='段落順序')
    style_code = models.CharField(default='1', max_length=30, verbose_name='版型代號')
    belong_article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE,
                                       related_name='paragraph_belong_article', verbose_name='段落對應之文章')

    class Meta:
        db_table = "paragraph"
