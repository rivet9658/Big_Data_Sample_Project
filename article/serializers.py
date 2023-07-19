# package
from urllib.parse import unquote
from rest_framework import serializers
# models
from article.models import ArticleModel, ArticleHaveImageModel, ArticleHaveEmojiModel, ArticleHaveMediaModel, \
    ArticleHaveTagModel
from paragraph.models import ParagraphModel
from comment.models import CommentModel
from emoji.models import EmojiModel
from media.models import MediaModel
from tag.models import TagModel
# constant
from big_data_sample_prj.constant import TAG_LIST


# 標題圖片資料序列化格式
class GetListArticleHaveImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleHaveImageModel
        fields = ('id', 'order', 'image', 'name', 'source')


class EditArticleHaveImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleHaveImageModel
        fields = ('order', 'image', 'source')

    def create(self, validated_data):
        now_requester = self.context.get('requester')
        belong_article = self.context.get('belong_article')
        validated_data['belong_article'] = belong_article
        validated_data['create_user'] = now_requester
        validated_data['updated_user'] = now_requester
        now_image = ArticleHaveImageModel.objects.create(**validated_data)
        now_image.name = unquote(now_image.image.url.split('/')[-1])
        now_image.save()
        return now_image


class GetArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='create_user.username', allow_null=True, label='作者')
    image_list = serializers.SerializerMethodField('get_article_title_image', label='文章標題圖片')
    have_paragraph = serializers.SerializerMethodField('get_article_have_paragraph', label='文章所含段落(id)')
    have_tag = serializers.SerializerMethodField('get_article_have_tag', label='文章所含標籤(name)')
    have_comment = serializers.SerializerMethodField('get_article_have_comment', label='文章所含留言(id)')

    class Meta:
        model = ArticleModel
        fields = ('id', 'author', 'title', 'introduction', 'publish_datetime', 'image_list', 'have_paragraph',
                  'have_tag', 'have_comment')

    # 取得文章標題圖片
    def get_article_title_image(self, instance):
        title_image_list = ArticleHaveImageModel.objects.filter(belong_article=instance, order=0)
        return_data = GetListArticleHaveImageSerializer(title_image_list, many=True).data
        return return_data

    # 取得文章所含段落(id)
    def get_article_have_paragraph(self, instance):
        return ParagraphModel.objects.filter(belong_article=instance).values('id', 'order')

    # 取得文章所含標籤(name)
    def get_article_have_tag(self, instance):
        return ArticleHaveTagModel.objects.filter(belong_article=instance).values_list('belong_tag__name', flat=True)

    # 取得文章所含留言(id)
    def get_article_have_comment(self, instance):
        return CommentModel.objects.filter(belong_article=instance).values_list('id', flat=True)


# 建立或更新文章時，所使用之段落序列化格式
class ParagraphListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParagraphModel
        fields = ('title', 'content', 'order', 'style_code')


# 建立或更新文章時，所使用之標籤序列化格式
class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ('name',)


class EditArticleSerializer(serializers.ModelSerializer):
    paragraph_list = serializers.ListField(write_only=True, child=ParagraphListSerializer(),
                                           label='文章段落列表')
    tag_list = serializers.ListField(write_only=True, child=TagListSerializer(), label=TAG_LIST)

    class Meta:
        model = ArticleModel
        fields = ('title', 'introduction', 'is_publish', 'publish_datetime', 'paragraph_list', 'tag_list')

    # 處理目標文章的段落資料
    def process_paragraph_list(self, article, paragraph_list, now_requester):
        paragraph_list.sort(key=lambda x: x['order'])
        # 取得文章原始段落資料
        original_paragraph_list = ParagraphModel.objects.filter(belong_article=article)
        original_order_list = list(original_paragraph_list.values_list('order', flat=True))
        original_order_list.sort()
        last_order = 0
        for paragraph_data in paragraph_list:
            paragraph_data['updated_user'] = now_requester
            # 如果給入資料順序未符合格式(例如1,2,3,4...，連續且不重複)，嘗試整理段落順序
            if paragraph_data['order'] == last_order:
                paragraph_data['order'] += 1
            elif paragraph_data['order'] != last_order + 1:
                paragraph_data['order'] = last_order + 1
            last_order = paragraph_data['order']
            # 判斷該段落是否存在於文章原始段落中
            filter_paragraph = original_paragraph_list.filter(order=paragraph_data['order'])
            if filter_paragraph.exists():  # 如果存在，則更新該段落資料
                filter_paragraph.update(**paragraph_data)
                if paragraph_data['order'] in original_order_list:
                    try:
                        original_order_list.remove(paragraph_data['order'])
                    except ValueError:
                        pass
            else:  # 如果不存在，則新增該段落資料
                paragraph_data['create_user'] = now_requester
                paragraph_data['belong_article'] = article
                ParagraphModel.objects.create(**paragraph_data)
        if len(original_order_list) > 0:  # 刪除文章原始段落中，不存在於新文章段落中的段落資料
            original_paragraph_list.filter(order__in=original_order_list).delete()

    # 處理目標文章的標籤資料
    def process_tag_list(self, article, tag_list, now_requester):
        # 取得文章原始標籤資料
        original_tag_list = ArticleHaveTagModel.objects.filter(belong_article=article)
        original_tag_id_list = list(original_tag_list.values_list('belong_tag_id', flat=True))
        for tag_data in tag_list:
            # 判斷該標籤是否存在於標籤列表內
            filter_tag = TagModel.objects.filter(name=tag_data['name'])
            if filter_tag.exists():  # 如果存在，則更新該標籤資料
                now_tag = filter_tag.first()
                if now_tag.id in original_tag_id_list:
                    try:
                        original_tag_id_list.remove(now_tag.id)
                    except ValueError:
                        pass
            else:  # 如果不存在，則新增該標籤資料
                tag_data['create_user'] = now_requester
                tag_data['updated_user'] = now_requester
                now_tag = TagModel.objects.create(**tag_data)
            # 判斷該標籤是否存在於文章原始標籤中，沒有則新增
            ArticleHaveTagModel.objects.get_or_create(belong_article=article, belong_tag=now_tag,
                                                      create_user=now_requester, updated_user=now_requester)
        if len(original_tag_id_list) > 0:  # 刪除文章原始標籤中，不存在於新文章標籤中的標籤資料
            original_tag_list.filter(belong_article=article, belong_tag_id__in=original_tag_id_list).delete()

    def create(self, validated_data):
        # 整理資料並建立文章
        paragraph_list = validated_data.pop('paragraph_list')
        tag_list = validated_data.pop('tag_list')
        now_requester = self.context['request'].user
        validated_data['create_user'] = now_requester
        validated_data['updated_user'] = now_requester
        article = ArticleModel.objects.create(**validated_data)
        self.process_paragraph_list(article, paragraph_list, now_requester)
        self.process_tag_list(article, tag_list, now_requester)
        return article

    def update(self, instance, validated_data):
        # 整理資料並更新文章
        now_requester = self.context['request'].user
        paragraph_list = validated_data.pop('paragraph_list')
        tag_list = validated_data.pop('tag_list')
        validated_data['updated_user'] = now_requester
        article = super().update(instance, validated_data)
        article.save()
        self.process_paragraph_list(article, paragraph_list, now_requester)
        self.process_tag_list(article, tag_list, now_requester)
        return article


class StatisticsArticleHaveEmojiSerializer(serializers.ModelSerializer):
    emoji_count = serializers.SerializerMethodField('article_have_emoji_count', label='文章含有表情')

    class Meta:
        model = ArticleModel
        fields = ('emoji_count',)

    def article_have_emoji_count(self, instance):
        return_data = []
        all_emoji = EmojiModel.objects.all()
        for emoji_data in all_emoji:
            emoji_count = ArticleHaveEmojiModel.objects.filter(belong_article=instance, belong_emoji=emoji_data).count()
            return_data.append({
                'emoji_code': emoji_data.code,
                'emoji_name': emoji_data.name,
                'count': emoji_count
            })

        return return_data


class AddArticleHaveEmojiSerializer(serializers.ModelSerializer):
    emoji_code = serializers.CharField(label='表情代碼')

    class Meta:
        model = ArticleHaveEmojiModel
        fields = ('emoji_code',)

    def create(self, validated_data):
        now_requester = self.context.get('requester')
        belong_article = self.context.get('belong_article')
        return ArticleHaveEmojiModel.objects.create(
            belong_article=belong_article,
            belong_emoji=EmojiModel.objects.filter(code=validated_data['emoji_code']).first(),
            create_user=now_requester,
            updated_user=now_requester
        )


class GetListArticleHaveTagSerializer(serializers.ModelSerializer):
    tag_list = serializers.SerializerMethodField('get_tag_list', label=TAG_LIST)

    class Meta:
        model = ArticleHaveTagModel
        fields = ('tag_list',)

    def get_tag_list(self, instance):
        return ArticleHaveTagModel.objects.filter(belong_article=instance).values_list('belong_tag__name', flat=True)


class EditArticleHaveTagSerializer(serializers.ModelSerializer):
    tag_list = serializers.ListField(write_only=True, child=TagListSerializer(), label=TAG_LIST)

    class Meta:
        model = ArticleHaveTagModel
        fields = ('tag_list',)

    def create(self, validated_data):
        now_requester = self.context.get('requester')
        belong_article = self.context.get('belong_article')
        for tag_data in validated_data['tag_list']:
            filter_tag = TagModel.objects.filter(name=tag_data['name'])
            if filter_tag.exists():
                filter_tag = filter_tag.first()
            else:
                filter_tag = TagModel.objects.create(
                    name=tag_data['name'],
                    create_user=now_requester,
                    updated_user=now_requester
                )
            check_have_tag = ArticleHaveTagModel.objects.filter(belong_article=belong_article,
                                                                belong_tag=filter_tag)
            if not check_have_tag.exists():
                ArticleHaveTagModel.objects.create(
                    belong_article=belong_article,
                    belong_tag=filter_tag,
                    create_user=now_requester,
                    updated_user=now_requester
                )
        return validated_data

    def update(self, instance, validated_data):
        now_requester = self.context['request'].user
        original_tag_queryset = ArticleHaveTagModel.objects.filter(belong_article=instance)
        original_tag_list = list(original_tag_queryset.values_list('belong_tag_id', flat=True))
        for tag_data in validated_data['tag_list']:
            filter_tag = TagModel.objects.filter(name=tag_data['name'])
            if filter_tag.exists():
                filter_tag = filter_tag.first()
            else:
                filter_tag = TagModel.objects.create(
                    name=tag_data['name'],
                    create_user=now_requester,
                    updated_user=now_requester
                )
            check_have_tag = original_tag_queryset.filter(belong_tag=filter_tag.id)
            if check_have_tag.exists():
                try:
                    original_tag_list.remove(filter_tag.id)
                except ValueError:
                    pass
            else:
                ArticleHaveTagModel.objects.create(
                    belong_article=instance,
                    belong_tag=filter_tag,
                    create_user=now_requester,
                    updated_user=now_requester
                )
        if len(original_tag_list) > 0:
            original_tag_queryset.filter(belong_tag_id__in=original_tag_list).delete()
        return validated_data


class GetListArticleHaveMediaSerializer(serializers.ModelSerializer):
    media_list = serializers.SerializerMethodField('get_media_list', label='媒體標籤列表')

    class Meta:
        model = ArticleHaveMediaModel
        fields = ('media_list',)

    def get_media_list(self, instance):
        return ArticleHaveMediaModel.objects.filter(belong_article=instance).values('belong_media__code',
                                                                                    'belong_media__name',
                                                                                    'belong_media__image',
                                                                                    'belong_media__image_name',
                                                                                    'belong_media__image_source')


class MediaListSerializer(serializers.ModelSerializer):
    report_url = serializers.CharField(label='媒體報導網址')

    class Meta:
        model = MediaModel
        fields = ('code', 'report_url')


class EditArticleHaveMediaSerializer(serializers.ModelSerializer):
    media_list = serializers.ListField(write_only=True, child=MediaListSerializer(), label='文章媒體列表')

    class Meta:
        model = ArticleHaveMediaModel
        fields = ('media_list',)

    def create(self, validated_data):
        now_requester = self.context.get('requester')
        belong_article = self.context.get('belong_article')
        for media_data in validated_data['media_list']:
            now_media_queryset = MediaModel.objects.filter(code=media_data['code'])
            if now_media_queryset.exists():
                now_media = now_media_queryset.first()
                check_have_media = ArticleHaveMediaModel.objects.filter(belong_article=belong_article,
                                                                        belong_media=now_media,
                                                                        report_url=media_data['report_url'])
                if not check_have_media.exists():
                    ArticleHaveMediaModel.objects.create(
                        belong_article=belong_article,
                        belong_media=now_media,
                        report_url=media_data['report_url'],
                        create_user=now_requester,
                        updated_user=now_requester
                    )
        return validated_data

    def update(self, instance, validated_data):
        now_requester = self.context['request'].user
        original_media_queryset = ArticleHaveMediaModel.objects.filter(belong_article=instance)
        original_tag_list = list(original_media_queryset.values('belong_media_id', 'report_url'))
        for media_data in validated_data['media_list']:
            now_media_queryset = MediaModel.objects.filter(code=media_data['code'])
            if now_media_queryset.exists():
                now_media = now_media_queryset.first()
                check_have_media = original_media_queryset.filter(belong_media=now_media,
                                                                  report_url=media_data['report_url'])
                if check_have_media.exists():
                    try:
                        original_tag_list.remove(
                            {'belong_media_id': now_media.id, 'report_url': media_data['report_url']})
                    except ValueError:
                        pass
                else:
                    ArticleHaveMediaModel.objects.create(
                        belong_article=instance,
                        belong_media=now_media,
                        report_url=media_data['report_url'],
                        create_user=now_requester,
                        updated_user=now_requester
                    )
        if len(original_tag_list) > 0:
            for original_media in original_tag_list:
                original_media_queryset.filter(belong_media_id=original_media['belong_media_id'],
                                               report_url=original_media['report_url']).delete()

        return validated_data
