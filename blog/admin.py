from django.contrib import admin
from blog.models import Detail,Category,About

class PostAdmin(admin.ModelAdmin):
    list_display=('title','content')
    search_fields=('title','content')
    list_filter=('title','content')
# Register your models here.
admin.site.register(Detail)
admin.site.register(Category)
admin.site.register(About)
