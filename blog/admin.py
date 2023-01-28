from django.contrib import admin
from .models import PostModel, ProfileModel ,GoalsModel , CommentModel, Category, Follower
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'updated', 'created']
    # prepopulated_fields = {'slug': ('name',)}

@admin.register(ProfileModel)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

@admin.register(GoalsModel)
class GoalsModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal', 'Timeline_objective', 'complete', 'created']

@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['user','title', 'content', 'date_stamp']

admin.site.register(CommentModel)

@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['follower','following', 'created_at']