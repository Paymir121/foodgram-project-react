import csv 
from pathlib import Path 

from django.conf import settings
from django.core.management.base import BaseCommand 

from recipy.models import Ingredient
from users.models import User 

TABLES = { 

    Ingredient: 'ingredients.csv', 
} 
def get_reader(file_name): 
    csv_path = Path(settings.INITIAL_DATA_DIR, file_name) 
    csv_file = open(csv_path, 'r', encoding='utf-8') 
    reader = csv.DictReader(csv_file, delimiter=',') 
    return reader 

class Command(BaseCommand): 
    def handle(self, *args, **options): 
        for model, csv_file in TABLES.items(): 
            csv_reader = get_reader(csv_file) 
            model.objects.bulk_create(model(**data) for data in csv_reader) 
        print('Import DONE')