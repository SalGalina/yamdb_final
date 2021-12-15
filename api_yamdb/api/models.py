from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from pytils.translit import slugify

from .managers import CreateSuperUserManager, Roles
from .validators import year_validator


class User(AbstractUser):
    USER = Roles.USER.value
    MODERATOR = Roles.MODERATOR.value
    ADMIN = Roles.ADMIN.value
    ROLES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin')
    ]
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
        null=True
    )

    email = models.EmailField(
        verbose_name='Эл.почта',
        max_length=100,
        unique=True,
        error_messages={
            'unique': 'Пользователь с такой почтой уже существует',
        },
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=50
    )
    bio = models.TextField(
        verbose_name='Жизнеописание',
        max_length=500,
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=ROLES,
        default=USER,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CreateSuperUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return f'{self.email[:20]}'


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=250
    )
    slug = models.SlugField(
        verbose_name='Адрес категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return f'{self.name[:100]} -- {self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super().save(*args, **kwargs)


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=250
    )
    slug = models.SlugField(
        verbose_name='Адрес жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return f'{self.name[:100]} -- {self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super().save(*args, **kwargs)


class Title(models.Model):
    """Произведения."""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=250
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        db_index=True,
        validators=[year_validator],
        default=timezone.datetime.today().year
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name', 'year']

    def __str__(self):
        return f'{self.category.name} {self.name}'


class Review(models.Model):
    """Отзывы на произведения."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                0,
                message='Минимальная оценка - 0'
            ),
            MaxValueValidator(
                10,
                message='Максимальная оценка - 10'
            )
        ],
        default=0
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'title'],
                name='unique_review_title'
            )
        ]

    def __str__(self):
        return f'{self.text[:100]} {self.author}'


class Comment(models.Model):
    """Комментарии к отзывам на произведения."""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв на произведение',
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        related_name='comments',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']
