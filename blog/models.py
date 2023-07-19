from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# Create your models here.

User = get_user_model()


# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    user_website = models.URLField(blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_report_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact - Name: {self.name}, Email: {self.email}, Phone: {self.phone}, Website: {self.user_website}, Message: {self.message},is_report_sent: {self.is_report_sent} "


from django.urls import reverse


class Group(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(max_length=400)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('group_posts', kwargs={'slug': self.slug})


class Post(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.text
