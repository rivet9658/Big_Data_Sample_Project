# package
from urllib.parse import unquote
from rest_framework import serializers
# models
from media.models import MediaModel


class GetMediaSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField('image_name_handle', label='測試')

    class Meta:
        model = MediaModel
        fields = ('id', 'code', 'name', 'image', 'image_name')

    def image_name_handle(self, instance):
        return unquote(instance.image.url.split('/')[-1])


class EditMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaModel
        fields = ('code', 'name', 'image')

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
        return now_media

    def update(self, instance, validated_data):
        now_requester = self.context['request'].user
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data['image']
        instance.updated_user = now_requester
        instance.save()
        return instance
