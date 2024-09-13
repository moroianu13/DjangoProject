from django.contrib import admin
from .models import Category, Item

# Register Category model
admin.site.register(Category)

# Register Item model (in case it's not already registered)
admin.site.register(Item)


