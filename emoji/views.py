# package
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# models
from emoji.models import EmojiModel
# serializers
from emoji.serializers import EmojiSerializer, GetEmojiSerializer, CreateEmojiSerializer
# permission
from emoji.permission import EmojiPermission


class EmojiView(viewsets.ModelViewSet):
    queryset = EmojiModel.objects.all()

    def get_permissions(self):
        permission_class = (IsAuthenticated, EmojiPermission)
        return [permission() for permission in permission_class]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetEmojiSerializer
        elif self.action in ['create']:
            return CreateEmojiSerializer
        elif self.action in ['update', 'partial_update']:
            return EmojiSerializer
        else:
            return GetEmojiSerializer

    @swagger_auto_schema(
        operation_summary='表情-獲取表情列表',
        operation_description='請求表情列表，過濾參數不輸入則那項不加入過濾',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('code', openapi.IN_QUERY, description="代號",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="名稱",
                              type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        filter_code = request.GET.get('code')
        filter_name = request.GET.get('name')
        if filter_code:
            queryset = EmojiModel.objects.filter(code__contains=filter_code)
        else:
            queryset = EmojiModel.objects.all()
        if filter_name:
            queryset = queryset.filter(name__contains=filter_name)
        serializer = GetEmojiSerializer(queryset, many=True)
        return Response({'msg': '獲得表情列表成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='表情-獲取單一表情',
        operation_description='請求單一表情',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = EmojiModel.objects.all()
        filter_queryset = get_object_or_404(queryset, id=pk)
        serializer = self.get_serializer(filter_queryset)
        return Response({'msg': '獲得單一表情成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='表情-新增表情',
        operation_description='新增表情',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'msg': '標籤新增失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '標籤新增成功', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='表情-更新表情',
        operation_description='更新指定表情',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def update(self, request, pk=None, *args, **kwargs):
        queryset = EmojiModel.objects.filter(id=pk).first()
        if not queryset:
            return Response({'msg': '查無更新目標資料', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'msg': '表情更新失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '表情更新成功', 'data': serializer.data},
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='不支援此操作',
        operation_description='不支援此操作',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def partial_update(self, request, pk=None, *args, **kwargs):
        return Response({'msg': '不支援此操作', 'data': []},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(
        operation_summary='表情-刪除表情',
        operation_description='刪除表情',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = EmojiModel.objects.filter(id=pk).first()
        if not queryset:
            return Response({'msg': '查無刪除目標資料', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        queryset.delete()
        return Response({'msg': '表情刪除成功', 'data': []},
                        status=status.HTTP_200_OK)
