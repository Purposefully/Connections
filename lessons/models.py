from django.db import models
from ..login import User

class Solo_Lesson(models.Models):
    title = models.CharField(max_length=45)
    image = models.ImageField(upload_to='images/')
    heading = models.CharField(max_length=45, default="What do you notice?")
    content = models.TextField(default="Share what you observe about the image.")
    list_item_number = models.IntegerField(default=0)
    likes_allowed = models.BooleanField(default=False)
    max_likes = models.IntegerField(default=0)
    justification_required = models.BooleanField(default=False)
    justification_text = models.TextField(default='I think this observation is significant because...')
    like_same_day = models.BooleanField(default=False)
    lesson_code = models.CharField(max_length=10)
    user = models.ForeignKey(User, related_name="solo_lessons", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

