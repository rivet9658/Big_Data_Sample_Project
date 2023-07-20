# package
from datetime import datetime
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# models
from article.models import ArticleModel
from comment.models import CommentModel
# serializers
from comment.serializers import GetCommentSerializer, EditCommentSerializer
# permission
from comment.permission import CommentPermission


class CommentView(viewsets.ModelViewSet):
    queryset = CommentModel.objects.all()

    def get_permissions(self):
        permission_class = (IsAuthenticated, CommentPermission)
        return [permission() for permission in permission_class]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetCommentSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EditCommentSerializer
        else:
            return GetCommentSerializer

    @swagger_auto_schema(
        operation_summary='評論-獲取評論列表',
        operation_description='請求評論列表，過濾參數不輸入則那項不加入過濾',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('belong_article', openapi.IN_QUERY, description="所屬文章(id)",
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter('start_leave_date', openapi.IN_QUERY, description="留言日期區間-開始",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('end_leave_date', openapi.IN_QUERY, description="留言日期區間-結束",
                              type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        filter_belong_article = request.GET.get('belong_article', -1)
        filter_start_date = request.GET.get('start_leave_date', '')
        filter_end_date = request.GET.get('end_leave_date', '')
        try:
            filter_belong_article = int(filter_belong_article)
        except ValueError:
            return Response({'msg': '文章id格式錯誤', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        if filter_belong_article > 0:
            queryset = CommentModel.objects.filter(belong_article_id=filter_belong_article)
        else:
            queryset = CommentModel.objects.all()
        if len(filter_start_date) > 0 and len(filter_end_date) > 0:
            try:
                filter_start_datetime = datetime.strptime(filter_start_date, '%Y-%m-%d')
                filter_end_datetime = datetime.strptime(filter_end_date, '%Y-%m-%d')
                filter_end_datetime = filter_end_datetime.replace(hour=23, minute=59, second=59)
                queryset = queryset.filter(leave_datetime__range=(filter_start_datetime, filter_end_datetime))
            except ValueError:
                return Response(
                    {'msg': '留言日期區間格式錯誤', 'data': []},
                    status=status.HTTP_400_BAD_REQUEST)
        serializer = GetCommentSerializer(queryset, many=True)
        return Response({'msg': '獲得評論列表成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='評論-獲取單一評論',
        operation_description='請求單一評論',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = CommentModel.objects.all()
        filter_queryset = get_object_or_404(queryset, id=pk)
        serializer = self.get_serializer(filter_queryset)
        return Response({'msg': '獲得單一評論成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='評論-新增評論',
        operation_description='新增指定文章之評論',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('belong_article', openapi.IN_QUERY, description="所屬文章(id)",
                              type=openapi.TYPE_NUMBER),
        ]
    )
    def create(self, request, *args, **kwargs):
        now_requester = request.user
        belong_article_id = request.GET.get('belong_article')
        try:
            belong_article_id = int(belong_article_id)
        except ValueError:
            return Response({'msg': '文章id格式錯誤', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        if belong_article_id <= 0:
            return Response({'msg': '請輸入正確的文章id格式', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        belong_article_queryset = ArticleModel.objects.filter(id=belong_article_id)
        if not belong_article_queryset.exists():
            return Response({'msg': '指定文章不存在', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        belong_article_data = belong_article_queryset.first()
        serializer = self.get_serializer(data=request.data, context={'belong_article': belong_article_data,
                                                                     'requester': now_requester})
        if not serializer.is_valid():
            return Response({'msg': '評論新增失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '評論新增成功', 'data': serializer.data},
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='評論-更新評論',
        operation_description='更新指定文章之評論',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def update(self, request, pk=None, *args, **kwargs):
        comment_queryset = CommentModel.objects.filter(id=pk)
        if not comment_queryset.exists():
            return Response({'msg': '查無更新目標資料', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        comment_data = comment_queryset.first()
        serializer = self.get_serializer(comment_data, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'msg': '評論更新失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '評論更新成功', 'data': serializer.data},
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
        operation_summary='評論-刪除評論',
        operation_description='刪除評論',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        comment_queryset = CommentModel.objects.filter(id=pk)
        if not comment_queryset.exists():
            return Response({'msg': '查無刪除目標資料', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        comment_data = comment_queryset.first()
        comment_data.delete()
        return Response({'msg': '評論刪除成功', 'data': []},
                        status=status.HTTP_200_OK)
