from django.core.management.base import BaseCommand
from food.models import MenuItem

ITEMS = [
    {'name': 'Cheese Pizza',  'price': 299, 'image': 'food/images/pizza.jpg',      'emoji': '🍕', 'category': 'pizza',  'description': 'Classic cheese pizza with rich tomato sauce and mozzarella.'},
    {'name': 'Veg Burger',    'price': 149, 'image': 'food/images/burger.jpg',     'emoji': '🍔', 'category': 'burger', 'description': 'Crispy veg patty with fresh veggies and our special sauce.'},
    {'name': 'Sandwich',      'price': 60,  'image': 'food/images/sandwhich.webp', 'emoji': '🥪', 'category': 'snack',  'description': 'Freshly made sandwich loaded with veggies and cheese.'},
    {'name': 'French Fries',  'price': 30,  'image': 'food/images/french.jpg',     'emoji': '🍟', 'category': 'snack',  'description': 'Golden crispy fries served hot with ketchup.'},
]

class Command(BaseCommand):
    help = 'Seed the database with default menu items'

    def handle(self, *args, **kwargs):
        for item in ITEMS:
            obj, created = MenuItem.objects.get_or_create(name=item['name'], defaults=item)
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f"{status}: {obj.name}")
        self.stdout.write(self.style.SUCCESS('Menu seeded successfully!'))
