from django.db import models
from fb_post.constants.reactions import Reaction
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class User(AbstractUser):
    userPhoto = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_body = models.CharField(max_length=200)
    posted_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk) + ", " + str(self.user) + ", " + self.post_body


class PostReactions(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reactionType = models.CharField(max_length=10, choices=Reaction.get_reactions())

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return str(self.post.postBody) + ", " + str(self.user) + ", " + self.reactionType


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_on = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.CharField(max_length=100)
    commentedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        if not self.commented_on == None:
            return str(self.pk) + ", " + str(self.commented_on.pk) + ", " + str(self.user) + ", " + self.commentText
        else:
            return str(self.pk) + ", " + str(self.user) + ", " + self.commentText


class CommentReactions(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reactionType = models.CharField(max_length=10, choices=Reaction.get_reactions())

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return str(self.comment.commentText) + ", " + str(self.user) + ", " + self.reactionType



class Person(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username_updated = models.CharField(max_length=60)
    uuid = models.UUIDField(unique=True)

