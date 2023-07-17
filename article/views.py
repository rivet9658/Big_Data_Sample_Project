# package
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# models
from article.models import ArticleModel, ArticleHaveTagModel
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
        operation_description='請求所有文章列表，過濾參數不輸入則那項不加入過濾',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('is_publish', openapi.IN_QUERY, description="是否發佈",
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('start_publish_date', openapi.IN_QUERY, description="發佈日期區間-開始",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('end_publish_date', openapi.IN_QUERY, description="發佈日期區間-結束",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('tags', openapi.IN_QUERY, description="標籤，請用,分隔",
                              type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        filter_is_publish = request.GET.get('is_publish')
        filter_start_date = request.GET.get('start_publish_date')
        filter_end_date = request.GET.get('end_publish_date')
        filter_tags = request.GET.get('tags')

        if filter_is_publish:
            filter_is_publish = filter_is_publish.lower() == 'true' or filter_is_publish == '1'
            queryset = ArticleModel.objects.filter(is_publish=filter_is_publish)
        else:
            queryset = ArticleModel.objects.all()
        if filter_start_date and filter_end_date:
            try:
                filter_start_datetime = datetime.strptime(filter_start_date, '%Y-%m-%d')
                filter_end_datetime = datetime.strptime(filter_end_date, '%Y-%m-%d')
                filter_end_datetime = filter_end_datetime.replace(hour=23, minute=59, second=59)
                queryset = queryset.filter(publish_datetime__range=(filter_start_datetime, filter_end_datetime))
            except ValueError:
                return Response(
                    {'msg': '發佈日期區間格式錯誤', 'data': 'start_publish_date or end_publish_date format error'},
                    status=status.HTTP_400_BAD_REQUEST)
        if filter_tags:
            now_article_have_tags = ArticleHaveTagModel.objects.filter(belong_article__in=queryset)
            now_tag_list = filter_tags.split(',')
            now_article = now_article_have_tags.filter(belong_tag__name__in=now_tag_list)
            queryset = queryset.filter(id__in=now_article.values('belong_article_id'))

        serializer = self.get_serializer(queryset, many=True)
        return Response({'msg': '獲得文章列表成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='文章-獲取單一文章',
        operation_description='請求單一文章',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = ArticleModel.objects.all()
        filter_queryset = get_object_or_404(queryset, id=pk)
        serializer = self.get_serializer(filter_queryset)
        return Response({'msg': '獲得單一文章成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='文章-新增文章',
        operation_description='新增文章',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'msg': '文章新增失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '文章新增成功', 'data': serializer.data},
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='文章-更新文章',
        operation_description='更新文章',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def update(self, request, pk=None, *args, **kwargs):
        queryset = ArticleModel.objects.filter(id=pk)
        if len(queryset) <= 0:
            return Response({'msg': '查無更新目標資料', 'data': 'not found data'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset[0], data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'msg': '文章更新失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '文章更新成功', 'data': serializer.data},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='文章-刪除文章',
        operation_description='刪除文章',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = ArticleModel.objects.filter(id=pk)
        if len(queryset) <= 0:
            return Response({'msg': '查無刪除目標資料', 'data': 'not found data'},
                            status=status.HTTP_400_BAD_REQUEST)
        queryset[0].delete()
        return Response({'msg': '文章刪除成功', 'data': 'success'},
                        status=status.HTTP_200_OK)
