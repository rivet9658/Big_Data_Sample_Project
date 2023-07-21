# package
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# models
from media.models import MediaModel
# serializers
from media.serializers import GetMediaSerializer, EditMediaSerializer
# permission
from media.permission import MediaPermission


class MediaView(viewsets.ModelViewSet):
    queryset = MediaModel.objects.all()

    def get_permissions(self):
        permission_class = (IsAuthenticated, MediaPermission)
        return [permission() for permission in permission_class]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetMediaSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EditMediaSerializer
        else:
            return GetMediaSerializer

    @swagger_auto_schema(
        operation_summary='媒體-獲取媒體列表',
        operation_description='請求媒體列表，過濾參數不輸入則那項不加入過濾',
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
        if len(filter_code) > 0:
            queryset = MediaModel.objects.filter(code__contains=filter_code)
        else:
            queryset = MediaModel.objects.all()
        if len(filter_name) > 0:
            queryset = queryset.filter(name__contains=filter_name)
        serializer = GetMediaSerializer(queryset, many=True)
        return Response({'msg': '獲得媒體列表成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='媒體-獲取單一媒體',
        operation_description='請求單一媒體',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = MediaModel.objects.all()
        filter_queryset = get_object_or_404(queryset, id=pk)
        serializer = self.get_serializer(filter_queryset)
        return Response({'msg': '獲得單一媒體成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='媒體-新增媒體',
        operation_description='新增媒體(資料格式form-data)',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def create(self, request, *args, **kwargs):
        media_code = request.data.get('code')
        media_name = request.data.get('name')
        image_file = request.FILES.get('image')
        image_source = request.data.get('image_source')
        need_create_data = {
            'code': media_code,
            'name': media_name,
            'image': image_file,
            'image_source': image_source
        }
        serializer = self.get_serializer(data=need_create_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': '新增媒體成功', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': '新增媒體失敗', 'data': request.data}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='媒體-更新媒體',
        operation_description='更新媒體(資料格式form-data)',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def update(self, request, pk=None, *args, **kwargs):
        media_queryset = MediaModel.objects.filter(id=pk)
        if not media_queryset.exists():
            return Response({'msg': '查無更新目標資料', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
        media_data = media_queryset.first()
        media_code = request.data.get('code')
        media_name = request.data.get('name')
        image_file = request.FILES.get('image')
        image_source = request.data.get('image_source')
        need_update_data = {
            'code': media_code,
            'name': media_name,
            'image': image_file,
            'image_source': image_source
        }
        serializer = self.get_serializer(media_data, data=need_update_data)
        if not serializer.is_valid():
            return Response({'msg': '更新媒體失敗', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '更新媒體成功', 'data': request.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='不支援此操作',
        operation_description='不支援此操作',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def partial_update(self, request, pk=None, *args, **kwargs):
        return Response({'msg': '不支援此操作', 'data': {}},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(
        operation_summary='媒體-刪除媒體',
        operation_description='刪除媒體',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        media_queryset = MediaModel.objects.filter(id=pk)
        if not media_queryset.exists():
            return Response({'msg': '查無刪除目標資料', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
        media_data = media_queryset.first()
        media_data.delete()
        return Response({'msg': '媒體刪除成功', 'data': {'id': pk}},
                        status=status.HTTP_200_OK)
