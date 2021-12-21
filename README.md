# CI и CD для yamdb_final

## Проект api_yamdb

### Описание

API для публикации оценок, отзывов и комментариев к произведениям.

### Технологии

- Python 3.7-slim
- Django 2.2.6
- Django REST Framework 3.12.4
- Django REST Framework SimpleJWT 4.7.2
- Gunicorn 20.1.0
- Nginx 1.21.3-alpine
- PostgreSQL 13.0-alpine

### Шаблон заполнения .env-файла

- DB_ENGINE= <сервер базы данных>
- POSTGRES_DB= <имя базы данных>
- POSTGRES_USER=
- POSTGRES_PASSWORD=
- DB_HOST= <название сервиса (контейнера базы данных)>
- DB_PORT= <порт для подключения к БД>

- DEBUG=
- SECRET_KEY=
- ALLOWED_HOSTS= <IP-адрес и доменные адреса сайта через пробел>

### Разворачивание и запуск проекта

- Установите Docker, Docker Compose

```bash
#!/bin/bash
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt update
sudo apt install \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce docker-compose -y
```

- Скачайте репозиторий с проектом с GitHub

```bash
#!/bin/bash
git clone git@github.com:SalGalina/yamdb_final.git
```

- Скачайте образ проекта с DockerHub

```bash
#!/bin/bash
sudo docker pull salgalina/yamdb_final:latest
```

- Настройте переменные окружения в .env файле и на GitHub Actions

- измените IP-адрес и доменные имена в infra/nginx/default.conf

- Локальный запуск приложения:

```bash
#!/bin/bash
sudo docker-compose up -d --build
```

- Запустите миграции:

```bash
#!/bin/bash
sudo docker-compose exec web python manage.py migrate
```

- Создайте суперпользователя:

```bash
#!/bin/bash
sudo docker-compose exec web python manage.py createsuperuser
```

- Соберите статику:

```bash
#!/bin/bash
sudo docker-compose exec web python manage.py collectstatic --no-input
```

- Загрузите данные в базу при необходимости:

```bash
#!/bin/bash
scp fixtures.json <username>@<domain_name or IP>:<home_dir>
python manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
python manage.py loaddata fixtures.json
```

### Авторы

Салошина Галина

![yamdb_workflow](https://github.com/SalGalina/yamdb_final/workflows/yamdb_workflow/badge.svg)
