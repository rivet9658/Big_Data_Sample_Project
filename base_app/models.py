# package
import os
from dotenv import load_dotenv
from django.db import models, transaction, IntegrityError, DatabaseError
from django.contrib.auth.models import User
from rest_framework.response import Response

load_dotenv()


# 當綁定的使用者被刪除時，將該資料綁到匿名使用者上
def get_anonymous_user():
    now_user, created = User.objects.get_or_create(username="anonymous")
    if created:
        now_user.set_password(os.getenv("ANONYMOUS_PASSWORD"))
        now_user.is_active = False
        now_user.save()
    return now_user


class BaseModel(models.Model):
    create_user = models.ForeignKey(User, on_delete=models.SET(get_anonymous_user), verbose_name='資料創建者',
                                    related_name='%(class)s_create_user')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='資料創建時間')
    updated_user = models.ForeignKey(User, on_delete=models.SET(get_anonymous_user), verbose_name='資料最後更新者',
                                     related_name='%(class)s_updated_user')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='資料最後更新時間')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.create_user_id:
            self.create_user = get_anonymous_user()
        if not self.updated_user_id:
            self.updated_user = get_anonymous_user()
        super().save(*args, **kwargs)

    # def save(
    #         self, force_insert=False, force_update=False, using=None, update_fields=None
    # ):
    #     try:
    #         super(BaseModel, self).save(force_insert, force_update, using, update_fields)
    #     except IntegrityError:  # saveException
    #         try:
    #             transaction.rollback()
    #         except (IntegrityError, DatabaseError):  # rollbackException
    #             return Response('回滾異常')
    #         return Response('儲存異常')
