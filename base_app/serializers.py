# package
from datetime import timedelta
# models
from base_app.models import BaseModel
# serializers
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    create_user_name = serializers.CharField(source='create_user.username', allow_null=True, label='資料創建人')
    updated_user_name = serializers.CharField(source='updated_user.username', allow_null=True, label='資料最後更新者')

    class Meta:
        model = BaseModel
        fields = ('create_user_name', 'create_datetime', 'updated_user_name', 'updated_datetime')
