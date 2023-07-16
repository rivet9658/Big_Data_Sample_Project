# package
from django.db import models
# models
from base_app.models import BaseModel


class EmojiModel(BaseModel):
    code = models.CharField(default='', max_length=50, verbose_name='表情代號')
    name = models.CharField(default='', max_length=50, verbose_name='表情名稱')

    class Meta:
        db_table = "emoji"
