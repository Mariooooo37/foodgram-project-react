import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

CORRECT_LEN_ROW = 2


class Command(BaseCommand):
    help = 'Загрузка тестовой БД'

    def handle(self, *args, **options):
        csv_file = os.path.join(
            settings.BASE_DIR, '..', 'data', 'ingredients.csv')
        with open(csv_file, encoding="utf8") as File:
            reader = csv.reader(File, delimiter=',')
            for row in reader:
                if len(row) == CORRECT_LEN_ROW and len(row[0]) > len(row[1]):
                    Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
