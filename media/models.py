# package
from django.db import models
# models
from base_app.models import BaseModel


# 圖片存放路徑
def media_image_path(instance, filename):
    belong_media_code = instance.code

    return f"static/images/media/{str(belong_media_code)}/{str(filename)}"


class MediaModel(BaseModel):
    code = models.CharField(default='', max_length=50, verbose_name='媒體代號')
    name = models.CharField(default='', max_length=50, verbose_name='媒體名稱')
    image = models.ImageField(upload_to=media_image_path, verbose_name='媒體圖片')
    image_name = models.CharField(default='', max_length=50, verbose_name='媒體圖片名稱(檔案名稱)')
    image_source = models.TextField(default='', verbose_name='媒體圖片來源(檔案來源)')

    class Meta:
        db_table = "media"
