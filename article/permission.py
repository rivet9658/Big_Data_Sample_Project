# package
from rest_framework import permissions

view_article_model = 'article.view_articlemodel'
add_article_model = 'article.add_articlemodel'
change_article_model = 'article.change_articlemodel'
delete_article_model = 'article.delete_articlemodel'


class ArticlePermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            permission_list = [view_article_model]
        elif view.action in ['create']:
            permission_list = [add_article_model]
        elif view.action in ['update', 'partial_update']:
            permission_list = [change_article_model]
        elif view.action in ['destroy']:
            permission_list = [delete_article_model]
        else:
            permission_list = []
        count = 0
        user = request.user
        for permission in permission_list:
            if user.has_perm(permission):
                count += 1
        return count >= len(permission_list)
