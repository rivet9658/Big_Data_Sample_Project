# package
from rest_framework import permissions

view_comment_model = 'paragraph.view_commentmodel'
add_comment_model = 'paragraph.add_commentmodel'
change_comment_model = 'paragraph.change_commentmodel'
delete_comment_model = 'paragraph.delete_commentmodel'


class CommentPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            permission_list = [view_comment_model]
        elif view.action in ['create']:
            permission_list = [add_comment_model]
        elif view.action in ['update', 'partial_update']:
            permission_list = [change_comment_model]
        elif view.action in ['destroy']:
            permission_list = [delete_comment_model]
        else:
            permission_list = []
        count = 0
        user = request.user
        for permission in permission_list:
            if user.has_perm(permission):
                count += 1
        return count >= len(permission_list)
