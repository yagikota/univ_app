from django.contrib import admin
from .models import Question, Response, Likes, QuestionImage
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Likes)
admin.site.register(QuestionImage)

admin.site.register(User, UserAdmin)
