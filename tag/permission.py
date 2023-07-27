# package
from rest_framework import permissions

view_tag_model = 'tag.view_tagmodel'
add_tag_model = 'tag.add_tagmodel'
change_tag_model = 'tag.change_tagmodel'
delete_tag_model = 'tag.delete_tagmodel'


class TagPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            permission_list = [view_tag_model]
        elif view.action in ['create']:
            permission_list = [add_tag_model]
        elif view.action in ['update', 'partial_update']:
            permission_list = [change_tag_model]
        elif view.action in ['destroy']:
            permission_list = [delete_tag_model]
        else:
            permission_list = []
        count = 0
        user = request.user
        for permission in permission_list:
            if user.has_perm(permission):
                count += 1
        return count >= len(permission_list)
