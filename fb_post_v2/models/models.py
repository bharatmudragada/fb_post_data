from django.db import models
from fb_post.constants.reactions import Reaction
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    profile_pic_url = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.CharField(max_length=200)
    posted_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk) + ", " + str(self.user) + ", " + str(self.post_content)


class PostReactions(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=Reaction.get_reactions())

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return str(self.post.post_content) + ", " + str(self.user) + ", " + str(self.reaction_type)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_on = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=100)
    commented_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        if not self.commented_on == None:
            return str(self.pk) + ", " + str(self.commented_on.pk) + ", " + str(self.user) + ", " + str(self.comment_text)
        else:
            return str(self.pk) + ", " + str(self.user) + ", " + str(self.comment_text)


class CommentReactions(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=Reaction.get_reactions())

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return str(self.comment.comment_text) + ", " + str(self.user) + ", " + str(self.reaction_type)

