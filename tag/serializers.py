# package
from rest_framework import serializers
# models
from tag.models import TagModel
# serializers
from article.serializers import TagListSerializer


class GetTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ('id', 'name')


class CreateTagSerializer(serializers.ModelSerializer):
    tag_list = serializers.ListField(write_only=True, child=TagListSerializer(), label='文章標籤列表')

    class Meta:
        model = TagModel
        fields = ('tag_list',)

    def create(self, validated_data):
        now_requester = self.context['request'].user
        for tag_data in validated_data['tag_list']:
            TagModel.objects.create(
                name=tag_data['name'],
                create_user=now_requester,
                updated_user=now_requester
            )
        return validated_data


class UpdateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ('name',)

    def update(self, instance, validated_data):
        now_requester = self.context['request'].user
        instance.name = validated_data.get('name', instance.name)
        instance.updated_user = now_requester
        instance.save()
        return instance
