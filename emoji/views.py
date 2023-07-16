# package
from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
# models
from emoji.models import EmojiModel
# serializers
from emoji.serializers import EmojiSerializer


class EmojiView(viewsets.ModelViewSet):
    queryset = EmojiModel.objects.all()

    def get_permissions(self):
        permission_class = (AllowAny,)
        return [permission() for permission in permission_class]

    def get_serializer_class(self):
        return EmojiSerializer
