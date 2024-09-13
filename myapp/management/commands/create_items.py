from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Item

class Command(BaseCommand):
    help = 'Create sample users and items'

    def handle(self, *args, **kwargs):
        
        user1, created = User.objects.get_or_create(username="user1")
        user2, created = User.objects.get_or_create(username="user2")
        user3, created = User.objects.get_or_create(username="user3")

       
        Item.objects.create(name="Item 1", user=user1)
        Item.objects.create(name="Item 2", user=user2)
        Item.objects.create(name="Item 3", user=user3)

        
        self.stdout.write(self.style.SUCCESS('Successfully created users and items'))

