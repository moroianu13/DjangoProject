from django.core.management.base import BaseCommand
from myapp.models import Item
from django.contrib.auth.models import User
from django.db.models import Value, BooleanField

class Command(BaseCommand):
    help = 'Run ORM practice queries'

    def handle(self, *args, **kwargs):
        # Task 2: Retrieve all items that do not belong to a specific user
        user2 = User.objects.get(username="user2")
        items = Item.objects.exclude(user=user2)
        self.stdout.write(self.style.SUCCESS(f"Items excluding user2: {items}"))

        # Task 3: Retrieve only the names of the items
        item_names = Item.objects.values_list('name', flat=True)
        self.stdout.write(self.style.SUCCESS(f"Item names: {list(item_names)}"))

        # Task 4: Order items by name in descending order
        ordered_items = Item.objects.order_by('-name')
        self.stdout.write(self.style.SUCCESS(f"Ordered items: {ordered_items}"))

        # Task 5: Filter Items by Name and User
        user1 = User.objects.get(username="user1")
        filtered_items = Item.objects.filter(name__startswith="Phone", user=user1)
        self.stdout.write(self.style.SUCCESS(f"Filtered items: {filtered_items}"))

        # Task 6: Annotate Items with Whether They Belong to a Specific User
        user1 = User.objects.get(username="user1")
        annotated_items = Item.objects.annotate(
            belongs_to_user=Value(True, output_field=BooleanField())
        ).filter(user=user1)
        self.stdout.write(self.style.SUCCESS(f"Annotated items: {annotated_items}"))

        # Task 7: Update Item Names for a Specific User
        user1 = User.objects.get(username="user1")
        Item.objects.filter(user=user1).update(name="Updated Item")
        self.stdout.write(self.style.SUCCESS("Updated item names for user1."))

        # Task 8: Count the Number of Items for a User
        count = Item.objects.filter(user=user1).count()
        self.stdout.write(self.style.SUCCESS(f"Number of items for user1: {count}"))

        # Task 9: Delete All Items for a Specific User
        Item.objects.filter(user=user2).delete()
        self.stdout.write(self.style.SUCCESS("Deleted all items for user2."))

        # Task 10: Update or Create an Item
        user3 = User.objects.get(username="user3")
        Item.objects.update_or_create(
            name="Special Item", 
            user=user3,
            defaults={'name': 'Updated Special Item'}
        )
        self.stdout.write(self.style.SUCCESS("Updated or created 'Special Item' for user3."))
