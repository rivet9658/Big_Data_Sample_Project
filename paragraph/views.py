# package
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# models
from article.models import ArticleModel
from paragraph.models import ParagraphModel
# serializers
from paragraph.serializers import GetParagraphSerializer, EditParagraphSerializer
# permission
from paragraph.permission import ParagraphPermission


class ParagraphView(viewsets.ModelViewSet):
    queryset = ParagraphModel.objects.all()

    def get_permissions(self):
        permission_class = (IsAuthenticated, ParagraphPermission)
        return [permission() for permission in permission_class]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetParagraphSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EditParagraphSerializer
        else:
            return GetParagraphSerializer

    @swagger_auto_schema(
        operation_summary='段落-獲取段落列表',
        operation_description='請求段落列表，過濾參數不輸入則那項不加入過濾',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('belong_article', openapi.IN_QUERY, description="所屬文章(id)",
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter('order', openapi.IN_QUERY, description="第幾段落",
                              type=openapi.TYPE_NUMBER),
        ]
    )
    def list(self, request, *args, **kwargs):
        filter_belong_article = request.GET.get('belong_article', -1)
        filter_order = request.GET.get('order', -1)
        try:
            filter_belong_article = int(filter_belong_article)
        except ValueError:
            return Response({'msg': '文章id格式錯誤', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
        if filter_belong_article > 0:
            queryset = ParagraphModel.objects.filter(belong_article_id=filter_belong_article)
        else:
            queryset = ParagraphModel.objects.all()
        try:
            filter_order = int(filter_order)
        except ValueError:
            return Response({'msg': '段落順序格式錯誤', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
        if filter_order > 0:
            queryset = queryset.filter(order=filter_order)
        serializer = GetParagraphSerializer(queryset, many=True)
        return Response({'msg': '獲得段落列表成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='段落-獲取單一段落',
        operation_description='請求單一段落',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = ParagraphModel.objects.all()
        filter_queryset = get_object_or_404(queryset, id=pk)
        serializer = self.get_serializer(filter_queryset)
        return Response({'msg': '獲得單一段落成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='段落-新增段落',
        operation_description='新增指定文章之段落',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('belong_article', openapi.IN_QUERY, description="所屬文章(id)",
                              type=openapi.TYPE_NUMBER),
        ]
    )
    def create(self, request, *args, **kwargs):
        now_requester = request.user
        belong_article_id = request.GET.get('belong_article', -1)
        try:
            belong_article_id = int(belong_article_id)
        except ValueError:
            return Response({'msg': '文章id格式錯誤', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
        if belong_article_id <= 0:
            return Response({'msg': '請輸入正確的所屬文章id', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
        belong_article_queryset = ArticleModel.objects.filter(id=belong_article_id)
        if not belong_article_queryset.exists():
            return Response({'msg': '指定文章不存在', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
        belong_article_data = belong_article_queryset.first()
        serializer = self.get_serializer(data=request.data, context={'belong_article': belong_article_data,
                                                                     'requester': now_requester})
        if not serializer.is_valid():
            return Response({'msg': '段落新增失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '段落新增成功', 'data': request.data},
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='段落-更新段落',
        operation_description='更新指定文章之段落',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def update(self, request, pk=None, *args, **kwargs):
        paragraph_queryset = ParagraphModel.objects.filter(id=pk)
        if not paragraph_queryset.exists():
            return Response({'msg': '查無更新目標資料', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
        paragraph_data = paragraph_queryset.first()
        serializer = self.get_serializer(paragraph_data, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'msg': '段落更新失敗', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': '段落更新成功', 'data': request.data},
                        status=status.HTTP_201_CREATED)

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
        operation_summary='段落-刪除段落',
        operation_description='刪除段落',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ]
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        paragraph_queryset = ParagraphModel.objects.filter(id=pk)
        if not paragraph_queryset.exists():
            return Response({'msg': '查無刪除目標資料', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
        paragraph_data = paragraph_queryset.first()
        paragraph_data.delete()
        return Response({'msg': '段落刪除成功', 'data': {'id': pk}},
                        status=status.HTTP_200_OK)
