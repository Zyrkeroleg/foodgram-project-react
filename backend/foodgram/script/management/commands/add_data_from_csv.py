import csv

from api.models import Ingredient, Tags
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            'backend/foodgram/ingredients.csv',
                newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=unit)
            self.stdout.write('Ingredients added successfully')
        with open('backend/foodgram/tags.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                name, color, slug = row
                Tags.objects.get_or_create(
                    name=name,
                    color=color,
                    slug=slug)
            self.stdout.write('Tags added succsessfylly')
