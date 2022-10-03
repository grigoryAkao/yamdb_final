import os
from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Review, Title, User


class Command(BaseCommand):
    """Загрузка в базу данных по модели Review.
      Для загрузки данных нужно указать путь к файлу или
      загрузка выполнится автоматически из DEFAULT_FILE_PATH.
      """

    DEFAULT_FILE_PATH = os.path.join(
        os.path.join(os.path.abspath('static'), 'data'),
        'review.csv'
    )

    help = 'Загружает данные из csv-файла в таблицу Review.'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, nargs='?', default=self.DEFAULT_FILE_PATH
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, encoding='utf-8') as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                _, created = Review.objects.get_or_create(
                    id=int(row['id']),
                    title=Title.objects.get(id=int(row['title_id'])),
                    text=row['text'],
                    author=User.objects.get(id=int(row['author'])),
                    score=int(row['score']),
                    pub_date=row['pub_date']
                )
        self.stdout.write(
            self.style.SUCCESS(
                f'Данные из {file_path} успешно загружены.'
            )
        )
