# package
from rest_framework import permissions

view_paragraph_model = 'paragraph.view_paragraphmodel'
add_paragraph_model = 'paragraph.add_paragraphmodel'
change_paragraph_model = 'paragraph.change_paragraphmodel'
delete_paragraph_model = 'paragraph.delete_paragraphmodel'


class ParagraphPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            permission_list = [view_paragraph_model]
        elif view.action in ['create']:
            permission_list = [add_paragraph_model]
        elif view.action in ['update', 'partial_update']:
            permission_list = [change_paragraph_model]
        elif view.action in ['destroy']:
            permission_list = [delete_paragraph_model]
        else:
            permission_list = []
        count = 0
        user = request.user
        for permission in permission_list:
            if user.has_perm(permission):
                count += 1
        return count >= len(permission_list)
