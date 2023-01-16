from django.contrib import admin
from .models import PostModel, ProfileModel, CommentModel, Category
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'updated', 'created']
    # prepopulated_fields = {'slug': ('name',)}

@admin.register(ProfileModel)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['user','title', 'content', 'date_stamp']

admin.site.register(CommentModel)