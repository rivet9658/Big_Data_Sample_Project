# package
from rest_framework import permissions

view_media_model = 'paragraph.view_mediamodel'
add_media_model = 'paragraph.add_mediamodel'
change_media_model = 'paragraph.change_mediamodel'
delete_media_model = 'paragraph.delete_mediamodel'


class MediaPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            permission_list = [view_media_model]
        elif view.action in ['create']:
            permission_list = [add_media_model]
        elif view.action in ['update', 'partial_update']:
            permission_list = [change_media_model]
        elif view.action in ['destroy']:
            permission_list = [delete_media_model]
        else:
            permission_list = []
        count = 0
        user = request.user
        for permission in permission_list:
            if user.has_perm(permission):
                count += 1
        return count >= len(permission_list)
