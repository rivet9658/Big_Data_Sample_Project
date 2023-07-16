# package
from django.db import models
# models
from base_app.models import BaseModel


class TagModel(BaseModel):
    code = models.CharField(default='', max_length=50, verbose_name='標籤代號')
    name = models.CharField(default='', max_length=50, verbose_name='標籤名稱')

    class Meta:
        db_table = "tag"
