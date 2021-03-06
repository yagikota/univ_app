from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:30]

    def get_responses(self):
        return self.responses.filter(parent=None)

class QuestionImage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='queston_image')
    image = models.ImageField(upload_to="image/", blank=True, null=True)


class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    body = models.TextField()
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE) # 返信に対する返信で使用
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:30]

    # この返信に対する返信を取得
    def get_responses(self):
        return Response.objects.filter(parent=self)

class Likes(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
