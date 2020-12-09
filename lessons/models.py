from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Name must be at least 2 characters long."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email address is invalid."
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters long."
        if postData['password'] != postData['confirm_password']:
            errors["pwd_match"] = "Password must match Re-type Password"
        return errors


class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Solo_Lesson(models.Model):
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

class Post(models.Model):
    content = models.TextField()
    number_likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name="posts", on_delete = models.CASCADE)
    solo_lesson = models.ForeignKey(Solo_Lesson, related_name="posts", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    justification = models.TextField()
    user = models.ForeignKey(User, related_name="likes", on_delete = models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Connect_Lesson(models.Model):
    title = models.CharField(max_length=45)
    heading = models.CharField(max_length=45, default="How are these connected?")
    content = models.TextField(default="Share at least one conjecture about how these representations are related.")
    likes_allowed = models.BooleanField(default=False)
    max_likes = models.IntegerField(default=0)
    justification_required = models.BooleanField(default=False)
    justification_text = models.TextField(default='I think this observation is significant because...')
    like_same_day = models.BooleanField(default=False)
    lesson_code = models.CharField(max_length=10)
    user = models.ForeignKey(User, related_name="solo_lessons", on_delete = models.CASCADE)
    lesson1 = models.ForeignKey(Solo_Lesson, related_name="connect_lessons", on_delete = models.CASCADE)
    lesson2 = models.ForeignKey(Solo_Lesson, related_name="connect_lessons", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)