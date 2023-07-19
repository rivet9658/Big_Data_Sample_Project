# package
from rest_framework import serializers
# models
from article.models import ArticleHaveImageModel
from paragraph.models import ParagraphModel
# serializers
from article.serializers import GetListArticleHaveImageSerializer


class GetParagraphSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField('get_paragraph_have_image', label='文章標題圖片')

    class Meta:
        model = ParagraphModel
        fields = ('id', 'title', 'content', 'order', 'style_code', 'belong_article', 'image_list')

    # 取得文章所含標籤(name)
    def get_paragraph_have_image(self, instance):
        now_image_list = ArticleHaveImageModel.objects.filter(belong_article=instance.belong_article,
                                                              order=instance.order)
        return_data = GetListArticleHaveImageSerializer(now_image_list, many=True).data
        return return_data


class EditParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParagraphModel
        fields = ('title', 'content', 'style_code')

    def create(self, validated_data):
        belong_article = self.context.get('belong_article')
        validated_data['belong_article'] = belong_article
        now_requester = self.context.get('requester')
        validated_data['create_user'] = now_requester
        validated_data['updated_user'] = now_requester
        now_article_have_paragraph = ParagraphModel.objects.filter(belong_article=validated_data['belong_article'])
        validated_data['order'] = now_article_have_paragraph.count() + 1
        return ParagraphModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        now_requester = self.context['request'].user
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.style_code = validated_data.get('style_code', instance.style_code)
        instance.updated_user = now_requester
        instance.save()
        return instance
