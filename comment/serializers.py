# package
from django.utils import timezone
from rest_framework import serializers
# models
from comment.models import CommentModel


class GetCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='create_user.username', allow_null=True, label='作者')

    class Meta:
        model = CommentModel
        fields = ('id', 'author', 'content', 'leave_datetime', 'belong_article')


class EditCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ('content',)

    def create(self, validated_data):
        belong_article = self.context.get('belong_article')
        validated_data['belong_article'] = belong_article
        now_requester = self.context.get('requester')
        validated_data['leave_datetime'] = timezone.now()
        validated_data['create_user'] = now_requester
        validated_data['updated_user'] = now_requester
        return CommentModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        now_requester = self.context['request'].user
        instance.content = validated_data['content']
        instance.updated_user = now_requester
        instance.save()
        return instance
