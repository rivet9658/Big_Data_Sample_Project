# package
from rest_framework import serializers
# models
from paragraph.models import ParagraphModel


class GetParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParagraphModel
        fields = ('id', 'title', 'content', 'order', 'style_code', 'belong_article')


class EditParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParagraphModel
        fields = ('title', 'content', 'order', 'style_code', 'belong_article')
