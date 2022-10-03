import os
from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import GenreTitle


class Command(BaseCommand):
    """Загрузка в базу данных по модели GenreTitle.
      Для загрузки данных нужно указать путь к файлу или
      загрузка выполнится автоматически из DEFAULT_FILE_PATH.
      """

    DEFAULT_FILE_PATH = os.path.join(
        os.path.join(os.path.abspath('static'), 'data'),
        'genre_title.csv'
    )

    help = 'Загружает данные из csv-файла в таблицу GenreTitle.'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, nargs='?', default=self.DEFAULT_FILE_PATH
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, encoding='utf-8') as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                _, created = GenreTitle.objects.get_or_create(
                    id=int(row['id']),
                    genre_id=row['genre_id'],
                    title_id=row['title_id'],
                )
        self.stdout.write(
            self.style.SUCCESS(
                f'Данные из {file_path} успешно загружены.'
            )
        )
