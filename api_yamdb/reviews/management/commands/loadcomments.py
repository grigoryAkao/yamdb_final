import os
from csv import DictReader

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import Comment, Review, User


class Command(BaseCommand):
    """Загрузка в базу данных по модели Comments.
      Для загрузки данных нужно указать путь к файлу или
      загрузка выполнится автоматически из DEFAULT_FILE_PATH.
      """

    DEFAULT_FILE_PATH = os.path.join(
        os.path.join(os.path.abspath('static'), 'data'),
        'comments.csv'
    )

    help = 'Загружает данные из csv-файла в таблицу Comments.'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, nargs='?', default=self.DEFAULT_FILE_PATH
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, encoding='utf-8') as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                author = get_object_or_404(User, id=row['author'])
                review = get_object_or_404(Review, id=row['review_id'])
                comment = Comment(
                    id=row['id'],
                    review=review,
                    text=row['text'],
                    author=author,
                    pub_date=row['pub_date']
                )
                comment.save()
            # for row in reader:
            #     review = get_object_or_404(Review, id=row['review_id'])
            #     _, created = Comment.objects.get_or_create(
            #         id=int(row['id']),
            #         review_id=review,
            #         # review_id=Review.objects.get(id=row['review_id']),
            #         text=row['text'],
            #         author=User.objects.get(id=int(row['author'])),
            #         pub_date=row['pub_date']
            #     )
        self.stdout.write(
            self.style.SUCCESS(
                f'Данные из {file_path} успешно загружены.'
            )
        )
