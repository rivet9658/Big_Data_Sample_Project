# package
from rest_framework import serializers
# models
from article.models import ArticleModel, ArticleHaveImageModel, ArticleHaveTagModel
from paragraph.models import ParagraphModel
from comment.models import CommentModel
from tag.models import TagModel


# 標題圖片資料序列化格式
class GetArticleHaveImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleHaveImageModel
        fields = ('id', 'name', 'source', 'image')


class GetArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='create_user.username', allow_null=True, label='作者')
    image_list = serializers.SerializerMethodField('get_article_title_file', label='文章標題圖片')
    have_paragraph = serializers.SerializerMethodField('get_article_have_paragraph', label='文章所含段落(id)')
    have_comment = serializers.SerializerMethodField('get_article_have_comment', label='文章所含留言(id)')

    class Meta:
        model = ArticleModel
        fields = ('id', 'author', 'title', 'introduction', 'publish_datetime', 'image_list', 'have_paragraph',
                  'have_comment')

    def get_article_title_file(self, instance):
        title_image_list = ArticleHaveImageModel.objects.filter(belong_article=instance, order=0)
        return_data = GetArticleHaveImageSerializer(title_image_list, many=True).data
        return return_data

    def get_article_have_paragraph(self, instance):
        return ParagraphModel.objects.filter(belong_article=instance).values('id', 'order')

    def get_article_have_comment(self, instance):
        return CommentModel.objects.filter(belong_article=instance).values('id')


# 建立或更新文章時，所使用之段落序列化格式
class ArticleEditParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParagraphModel
        fields = ('title', 'content', 'order', 'style_code')


# 建立或更新文章時，所使用之標籤序列化格式
class ArticleEditTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ('name',)


class EditArticleSerializer(serializers.ModelSerializer):
    paragraph_list = serializers.ListField(write_only=True, child=ArticleEditParagraphSerializer(),
                                           label='文章段落列表')
    tag_list = serializers.ListField(write_only=True, child=ArticleEditTagSerializer(), label='文章標籤列表')

    class Meta:
        model = ArticleModel
        fields = ('title', 'introduction', 'is_publish', 'publish_datetime', 'paragraph_list', 'tag_list')

    # 處理目標文章的段落資料
    def process_paragraph_list(self, article, paragraph_list, now_requester):
        original_paragraph_list = ParagraphModel.objects.filter(belong_article=article)
        original_order_list = list(original_paragraph_list.values_list('order', flat=True))
        for paragraph_data in paragraph_list:
            paragraph_data['updated_user'] = now_requester
            filter_paragraph = original_paragraph_list.filter(order=paragraph_data['order'])
            if filter_paragraph.exists():
                filter_paragraph.update(**paragraph_data)
                if paragraph_data['order'] in original_order_list:
                    original_order_list.remove(paragraph_data['order'])
            else:
                paragraph_data['create_user'] = now_requester
                paragraph_data['belong_article'] = article
                ParagraphModel.objects.create(**paragraph_data)
        if len(original_order_list) > 0:
            original_paragraph_list.filter(order__in=original_order_list).delete()

    # 處理目標文章的標籤資料
    def process_tag_list(self, article, tag_list, now_requester):
        original_tag_list = ArticleHaveTagModel.objects.filter(belong_article=article)
        original_tag_id_list = list(original_tag_list.values_list('belong_tag_id', flat=True))
        for tag_data in tag_list:
            filter_tag = TagModel.objects.filter(name=tag_data['name'])
            if filter_tag.exists():
                now_tag = filter_tag.first()
                if now_tag.id in original_tag_id_list:
                    original_tag_id_list.remove(now_tag.id)
            else:
                tag_data['create_user'] = now_requester
                tag_data['updated_user'] = now_requester
                now_tag = TagModel.objects.create(**tag_data)
            ArticleHaveTagModel.objects.create(belong_article=article, belong_tag=now_tag,
                                               create_user=now_requester, updated_user=now_requester)
        if len(original_tag_id_list) > 0:
            original_tag_list.filter(belong_article=article, belong_tag_id__in=original_tag_id_list).delete()

    def create(self, validated_data):
        now_requester = self.context['request'].user
        paragraph_list = validated_data.pop('paragraph_list')
        tag_list = validated_data.pop('tag_list')
        validated_data['create_user'] = now_requester
        validated_data['updated_user'] = now_requester
        article = ArticleModel.objects.create(**validated_data)
        self.process_paragraph_list(article, paragraph_list, now_requester)
        self.process_tag_list(article, tag_list, now_requester)
        return article

    def update(self, instance, validated_data):
        now_requester = self.context['request'].user
        paragraph_list = validated_data.pop('paragraph_list')
        tag_list = validated_data.pop('tag_list')
        validated_data['updated_user'] = now_requester
        article = super().update(instance, validated_data)
        article.save()
        self.process_paragraph_list(article, paragraph_list, now_requester)
        self.process_tag_list(article, tag_list, now_requester)
        return article
