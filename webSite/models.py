from django.db import models
import datetime
from django.utils import timezone


class Category(models.Model):
    id = models.AutoField(primary_key=True,)
    CategoryName = models.TextField()

    def __str__(self):
        return self.CategoryName


class Post(models.Model):
    PostTitle = models.TextField()
    PostDesc = models.TextField()
    PostDate = models.DateTimeField(default= timezone.now)
    PostCategory = models.OneToOneField(Category,on_delete=models.CASCADE)
    Tags = models.TextField()

    def __str__(self):
        return self.PostTitle

class Comment(models.Model):
    AuthorName = models.TextField()
    Title = models.TextField()
    Description = models.TextField()
    SendDate = models.DateTimeField(default=timezone.now)
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.Title