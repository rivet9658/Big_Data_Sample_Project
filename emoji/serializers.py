# package
from rest_framework import serializers
# models
from emoji.models import EmojiModel


class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmojiModel
        fields = ('code', 'name')

    def update(self, instance, validated_data):
        now_requester = self.context['request'].user
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.updated_user = now_requester
        instance.save()
        return instance


class GetEmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmojiModel
        fields = ('id', 'code', 'name')


class CreateEmojiSerializer(serializers.ModelSerializer):
    emoji_list = serializers.ListField(write_only=True, child=EmojiSerializer(), label='表情列表')

    class Meta:
        model = EmojiModel
        fields = ('emoji_list',)

    def create(self, validated_data):
        now_requester = self.context['request'].user
        for emoji_data in validated_data['emoji_list']:
            EmojiModel.objects.create(
                code=emoji_data['code'],
                name=emoji_data['name'],
                create_user=now_requester,
                updated_user=now_requester
            )
        return validated_data
