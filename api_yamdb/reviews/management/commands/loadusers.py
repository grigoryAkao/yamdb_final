import os
from csv import DictReader

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Загрузка в базу данных по модели User.
    Для загрузки данных нужно указать путь к файлу или
    загрузка выполнится автоматически из DEFAULT_FILE_PATH.
    """

    DEFAULT_FILE_PATH = os.path.join(
        os.path.join(os.path.abspath('static'), 'data'),
        'users.csv'
    )

    help = 'Загружает данные из csv-файла в таблицу User.'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, nargs='?', default=self.DEFAULT_FILE_PATH
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, encoding='utf-8') as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                _, created = User.objects.get_or_create(
                    id=int(row['id']),
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
        self.stdout.write(
            self.style.SUCCESS(
                f'Данные из {file_path}  загружены в базу данных'
            )
        )
