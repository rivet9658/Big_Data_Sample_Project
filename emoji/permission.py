# package
from rest_framework import permissions

view_emoji_model = 'emoji.view_emojimodel'
add_emoji_model = 'emoji.add_emojimodel'
change_emoji_model = 'emoji.change_emojimodel'
delete_emoji_model = 'emoji.delete_emojimodel'


class EmojiPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            permission_list = [view_emoji_model]
        elif view.action in ['create']:
            permission_list = [add_emoji_model]
        elif view.action in ['update', 'partial_update']:
            permission_list = [change_emoji_model]
        elif view.action in ['destroy']:
            permission_list = [delete_emoji_model]
        else:
            permission_list = []
        count = 0
        user = request.user
        for permission in permission_list:
            if user.has_perm(permission):
                count += 1
        return count >= len(permission_list)
