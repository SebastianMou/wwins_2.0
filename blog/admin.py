from django.contrib import admin
from .models import PostModel, ProfileModel, CommentModel
# Register your models here.
@admin.register(ProfileModel)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['user','title', 'content', 'date_stamp']

admin.site.register(CommentModel)