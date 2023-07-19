# package
from urllib.parse import unquote
from rest_framework import serializers
# models
from media.models import MediaModel


class GetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaModel
        fields = ('id', 'code', 'name', 'image', 'image', 'image_name', 'image_source')


class EditMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaModel
        fields = ('code', 'name', 'image', 'image_source')

    def create(self, validated_data):
        now_requester = self.context['request'].user
        now_media = MediaModel.objects.create(
            code=validated_data['code'],
            name=validated_data['name'],
            create_user=now_requester,
            updated_user=now_requester
        )
        now_media.image = validated_data['image']
        now_media.save()
        now_media.image_name = unquote(now_media.image.url.split('/')[-1])
        now_media.image_source = validated_data['image_source']
        now_media.save()
        return now_media

    def update(self, instance, validated_data):
        now_requester = self.context['request'].user
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data['image']
        instance.save()
        instance.image_name = unquote(instance.image.url.split('/')[-1])
        instance.image_source = validated_data['image_source']
        instance.updated_user = now_requester
        instance.save()
        return instance
