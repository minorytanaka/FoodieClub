import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='Путь к CSV-файлу для импорта')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Ingredient.objects.create(
                    name=row['name'],
                    measurement_unit=row['measurement_unit']
                )
        self.stdout.write(self.style.SUCCESS(
            'Данные успешно импортированы в базу!')
        )
