# package
from rest_framework.decorators import action
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
        operation_summary='段落-獲取所有段落列表',
        operation_description='請求所有段落列表，過濾參數不輸入則那項不加入過濾',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('belong_article', openapi.IN_QUERY, description="所屬文章(id)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('order', openapi.IN_QUERY, description="第幾段落",
                              type=openapi.TYPE_NUMBER),
        ]
    )
    def list(self, request, *args, **kwargs):
        filter_belong_article = request.GET.get('belong_article')
        filter_order = request.GET.get('order')
        if filter_belong_article:
            queryset = ParagraphModel.objects.filter(belong_article_id=filter_belong_article)
        else:
            queryset = ParagraphModel.objects.all()
        if filter_order:
            queryset = queryset.filter(order=filter_order)
        serializer = GetParagraphSerializer(queryset, many=True)
        return Response(serializer.data)

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
