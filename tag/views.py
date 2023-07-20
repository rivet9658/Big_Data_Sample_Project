# package
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# models
from tag.models import TagModel
# serializers
from tag.serializers import GetTagSerializer, CreateTagSerializer, UpdateTagSerializer
# permission
from tag.permission import TagPermission


class TagView(viewsets.ModelViewSet):
    queryset = TagModel.objects.all()

    def get_permissions(self):
        permission_class = (IsAuthenticated, TagPermission)
        return [permission() for permission in permission_class]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetTagSerializer
        elif self.action in ['create']:
            return CreateTagSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateTagSerializer
        else:
            return GetTagSerializer

    @swagger_auto_schema(
        operation_summary='標籤-獲取標籤列表',
        operation_description='請求標籤列表，過濾參數不輸入則那項不加入過濾',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="名稱",
                              type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        filter_name = request.GET.get('name')
        if len(filter_name) > 0:
            queryset = TagModel.objects.filter(name__contains=filter_name)
        else:
            queryset = TagModel.objects.all()
        serializer = GetTagSerializer(queryset, many=True)
        return Response({'msg': '獲得標籤列表成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='標籤-獲取單一標籤',
        operation_description='請求單一標籤',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = TagModel.objects.all()
        filter_queryset = get_object_or_404(queryset, id=pk)
        serializer = self.get_serializer(filter_queryset)
        return Response({'msg': '獲得單一標籤成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='標籤-新增標籤',
        operation_description='新增標籤',
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
        operation_summary='標籤-更新標籤',
        operation_description='更新指定標籤',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def update(self, request, pk=None, *args, **kwargs):
        tag_queryset = TagModel.objects.filter(id=pk)
        if not tag_queryset.exists():
            return Response({'msg': '查無更新目標資料', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        tag_data = tag_queryset.first()
        serializer = self.get_serializer(tag_data, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'msg': '標籤更新失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '標籤更新成功', 'data': serializer.data},
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
        operation_summary='標籤-刪除標籤',
        operation_description='刪除標籤',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        tag_queryset = TagModel.objects.filter(id=pk)
        if not tag_queryset.exists():
            return Response({'msg': '查無刪除目標資料', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        tag_data = tag_queryset.first()
        tag_data.delete()
        return Response({'msg': '標籤刪除成功', 'data': []},
                        status=status.HTTP_200_OK)
