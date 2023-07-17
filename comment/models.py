# package
from django.db import models
from django.utils import timezone
# models
from base_app.models import BaseModel
from article.models import ArticleModel


class CommentModel(BaseModel):
    content = models.TextField(default='', verbose_name='留言內容')
    leave_datetime = models.DateTimeField(default=timezone.now, verbose_name='留言日期')
    belong_article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE,
                                       related_name='comment_belong_article', verbose_name='留言對應之文章')

    class Meta:
        db_table = "comment"
