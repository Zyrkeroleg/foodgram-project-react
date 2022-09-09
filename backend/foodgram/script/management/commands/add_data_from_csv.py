import csv
from django.core.management.base import BaseCommand
from api.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            './ingredients.csv',
                newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=unit)
            self.stdout.write('Successful')
