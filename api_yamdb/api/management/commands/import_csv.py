import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from rest_framework.generics import get_object_or_404
from api.models import Category, Comment, Genre, Review, Title, User

# Использование:
# 1. отредактировать список app_models, теми файлами, которые надо загрузить.
# Имена файлов (без разрешения) должны точно соответствовать именам моделей
# в нижнем регистре.
# 2. имена полей таблиц базы данных и заголовков в csv файле должны точно
# соответстовать
# 3. все поля таблицы базы данных, которые не заполняются из csv должны иметь
# возможность быть пустыми или Null
# 4. запустить файл импорта командой
# python manage.py import_csv [-dd] [-o]


class Command(BaseCommand):
    help = 'Загрузка данных в базу'

    def add_arguments(self, parser):
        parser.add_argument(
            '-dd', '--data_dir',
            default=os.path.join(
                os.path.dirname(settings.BASE_DIR), 'data\\'),
            help="Директроия начальных данных для загрузки")

    def handle(self, *args, **kwargs):
        data_dir = kwargs['data_dir']

        app_models = {
            'user': User,
            'category': Category,
            'genre': Genre,
            'title': Title,
            'review': Review,
            'comment': Comment,
            'title_genre': Title,
        }

        for file_name, model in app_models.items():
            with open(
                f'{data_dir}{file_name}.csv', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(
                    csv_file, delimiter=',', quotechar='"')

                for line in reader:
                    if file_name == 'title_genre':
                        title = get_object_or_404(
                            Title,
                            pk=line['title_id']
                        )
                        title.genre.add(line['genre_id'])
                    else:
                        model.objects.create(**line)
            csv_file.close()
            self.stdout.write(
                f'Данные добавлены в таблицу api_{file_name}')
