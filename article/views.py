# package
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
# models
from article.models import ArticleModel
# serializers
from article.serializers import GetArticleSerializer, EditArticleSerializer
# permission
from article.permission import ArticlePermission


class ArticleView(viewsets.ModelViewSet):
    queryset = ArticleModel.objects.all()

    def get_permissions(self):
        permission_class = (IsAuthenticated, ArticlePermission)
        return [permission() for permission in permission_class]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetArticleSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EditArticleSerializer
        else:
            return GetArticleSerializer

    @swagger_auto_schema(
        operation_summary='文章-獲取所有文章列表',
        operation_description='請求所有文章列表',
    )
    def list(self, request, *args, **kwargs):
        queryset = ArticleModel.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='文章-獲取單一文章',
        operation_description='請求單一文章',
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = ArticleModel.objects.all()
        filter_queryset = get_object_or_404(queryset, id=pk)
        serializer = self.get_serializer(filter_queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='文章-新增文章',
        operation_description='新增文章',
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error_msg': '文章新增失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'success_msg': '文章新增成功', 'data': serializer.data},
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='文章-更新文章',
        operation_description='更新文章',
    )
    def update(self, request, pk=None, *args, **kwargs):
        queryset = ArticleModel.objects.filter(id=pk)
        if len(queryset) <= 0:
            return Response({'error_msg': '查無更新目標資料', 'data': 'not found data'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset[0], data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'error_msg': '文章更新失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'success_msg': '文章更新成功', 'data': serializer.data},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='文章-刪除文章',
        operation_description='刪除文章',
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = ArticleModel.objects.filter(id=pk)
        if len(queryset) <= 0:
            return Response({'error_msg': '查無刪除目標資料', 'data': 'not found data'},
                            status=status.HTTP_400_BAD_REQUEST)
        queryset[0].delete()
        return Response({'success_msg': '文章刪除成功', 'data': 'success'},
                        status=status.HTTP_200_OK)
