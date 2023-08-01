import csv 
from pathlib import Path 

from django.conf import settings
from django.core.management.base import BaseCommand 

from recipy.models import Ingredient


def get_reader(file_name): 
    csv_path = Path(settings.INITIAL_DATA_DIR, file_name) 
    csv_file = open(csv_path, 'r', encoding='utf-8') 
    reader = csv.DictReader(csv_file, delimiter=',') 
    return reader 


class Command(BaseCommand): 

    def handle(self, *args, **options):
        csv_reader = get_reader("ingredients.csv")
        next(csv_reader)
        Ingredient.objects.bulk_create([Ingredient(name=ingredeint['name'],
                                                       measurement_unit=ingredeint['measurement_unit']) 
                                                       for ingredeint in csv_reader]) 
