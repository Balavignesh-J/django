from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

class Detail(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField(null=True)
    img_url=models.ImageField(upload_to="post/images" ,null=True)
    created_at=models.DateTimeField(default=timezone.now)
    slug=models.SlugField(unique=True,blank=True,default='')
    category=models.ForeignKey("blog.Category", on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE ,null=True)

    def save(self, *args, **kwargs):
       self.slug=slugify(self.title)
       super().save(*args, **kwargs)

    @property
    def format_img_url(self):
        return self.img_url if self.img_url.__str__().startswith(("https://","http://")) else self.img_url.url

    def __str__(self):
        return self.title

class Category(models.Model):
    name=models.TextField()

    def __str__(self):
        return self.name

class About(models.Model):
    content=models.TextField()

    def __str__(self):
        return self.content