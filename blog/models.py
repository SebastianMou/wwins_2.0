# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, db_index=True, null=True)
    category_img = models.ImageField(upload_to='media', default='default.png', null=True)
    discription = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(default='Hi my name is ... my trying to improve, create, learn, build', max_length=355)
    user_image = models.ImageField(upload_to='media', validators=[FileExtensionValidator(['png', 'jpg'])], default='default.png')
    followed_categories = models.ManyToManyField(Category, blank=True, related_name='followed_by')

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

class GoalsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    goal = models.CharField(max_length=100, null=True)
    content = RichTextField()
    STATUS_CHOICES = (
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('2029', '2029'),
        ('2030', '2030'),
        ('2031', '2031'),
        ('2032', '2032'),
        ('2033', '2033'),
        ('2034', '2034'),
        ('2035', '2035'),
    )
    Timeline_objective = models.CharField(max_length=20, choices=STATUS_CHOICES, default='2023')
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.goal

class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    date_stamp = models.DateTimeField(auto_now_add=True, null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content = RichTextField()

    class Meta:
        ordering = ['-date_stamp']

    def __str__(self) -> str:
        return self.content
    
    def children(self):
        return CommentModel.objects.filter(parent_comment=self)

    @property
    def is_parent(self):
        if self.parent_comment is not None: 
            return False
        return True

class ReplyModel(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE)

class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='followers', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following', 'category')

class CategoryFollower(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
