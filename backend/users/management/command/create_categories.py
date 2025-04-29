from django.core.management.base import BaseCommand
from users.models import Category

class Command(BaseCommand):
    help = 'Create initial categories for user interests'

    def handle(self, *args, **kwargs):
        categories = [
            "Technology",
            "Science",
            "Art",
            "Music",
            "Sports",
            "Travel",
            "Food",
            "Fashion",
            "Movies",
            "Books",
            "Photography",
            "Gaming",
            "Fitness",
            "Education",
            "Business"
        ]
        
        created_count = 0
        
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} new categories'))