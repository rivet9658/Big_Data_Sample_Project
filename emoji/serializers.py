# package
from django.utils import timezone
from rest_framework import serializers
# models
from emoji.models import EmojiModel


class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmojiModel
        fields = ('id', 'code', 'name')

    def create(self, validated_data):
        validated_data['create_user'] = self.context['request'].user
        validated_data['updated_user'] = self.context['request'].user
        emoji = EmojiModel.objects.create(**validated_data)
        return emoji
