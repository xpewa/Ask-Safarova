from django.contrib import admin
from .models import Profile, Question, Tag, Answer

# Register your models here.
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)