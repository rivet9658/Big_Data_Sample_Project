"""big_data_sample_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# package
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi
# views
from article.views import ArticleView
from paragraph.views import ParagraphView
from comment.views import CommentView
from emoji.views import EmojiView
from media.views import MediaView
from tag.views import TagView


# schema generator
class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        return schema


# schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Sample Prj API",
        default_version='v1.0',
        description="Sample Prj 的所有 API 文檔",
        contact=openapi.Contact(email="bo.chen.lin8831@gmail.com"),
        license=openapi.License(name="BO CHEN LIN License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=SchemaGenerator
)

view_list = [
    {'url_name': 'article', 'view': ArticleView, 'basename': 'article'},
    {'url_name': 'paragraph', 'view': ParagraphView, 'basename': 'paragraph'},
    {'url_name': 'comment', 'view': CommentView, 'basename': 'comment'},
    {'url_name': 'emoji', 'view': EmojiView, 'basename': 'emoji'},
    {'url_name': 'media', 'view': MediaView, 'basename': 'media'},
    {'url_name': 'tag', 'view': TagView, 'basename': 'tag'},
]

# register view
register_router = DefaultRouter()
for view in view_list:
    register_router.register(view['url_name'], view['view'], view['basename'])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/sample_prj/', schema_view.with_ui('swagger', cache_timeout=0),
         name='big_data_sample_prj_swagger_schema'),
    path('api/sample_prj/', include(register_router.urls)),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
