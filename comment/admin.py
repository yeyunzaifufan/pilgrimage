from django.contrib import admin


# Register your models here.
from comment.models import Comment
from pilgrimage.base_admin import BaseOwnerAdmin
from pilgrimage.custom_site import custom_site


@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
