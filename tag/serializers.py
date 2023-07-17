# package
from rest_framework import serializers
# models
from article.models import ArticleModel


class GetTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = ('id', 'name')


class EditTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = 'name'
