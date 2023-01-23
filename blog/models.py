# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, null=True)
    discription = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('category_list', args=[self.slug])

    def __str__(self) -> str:
        return self.name

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(default='Hi my name is ... my trying to improve, create, learn, build', max_length=355)
    user_image = models.ImageField(upload_to='media', validators=[FileExtensionValidator(['png', 'jpg'])], default='default.png')

    def __str__(self) -> str:
        return f'profile of{self.user.username}'

class PostModel(models.Model):
    category = models.ForeignKey(Category, related_name='post', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    content = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date_stamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    class Meta:
        ordering = ['-date_stamp']

    def total_likes(self):
        return self.likes.count()

    def comment_cout(self):
        return self.commentmodel_set.all().count()

    def comments(self):
        return self.commentmodel_set.all()

    def __str__(self) -> str:
        return self.content

class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    date_stamp = models.DateTimeField(auto_now_add=True, null=True)
    content = RichTextField()

    class Meta:
        ordering = ['-date_stamp']

    def __str__(self) -> str:
        return self.content

class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
