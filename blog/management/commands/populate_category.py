from blog.models import Category
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help='populate category'
    
    def handle(self, *args, **options):
        Category.objects.all().delete()

        Categories=['sports','music','health','education','technology']

        for c in Categories:
            Category.objects.create(name=c)