import csv
from api.models import Ingredients

with open('/home/zyrker/Dev/foodgram-project-react/backend/foodgram/ingredients.csv', newline='') as File:  
    reader = csv.reader(File)
    for row in reader:
        name, unit = row
        Ingredients.objects.get_or_create(
            name=name,
            measurement_unit=unit)
