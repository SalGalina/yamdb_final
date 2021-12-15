from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Администрирование Пользователей."""

    list_display = (
        'pk',
        'role',
        'email',
        'confirmation_code',
        'username',
        'first_name',
        'last_name',
        'bio'
    )
    search_fields = ('email', 'last_name', 'first_name')
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Администрирование Категорий."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Администрирование Жанров."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Администрирование Произведений."""

    list_display = (
        'pk',
        'year',
        'name',
        'description',
        'category')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'description')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Администрирование Отзывов на произведения."""

    list_display = (
        'pk',
        'text',
        'author',
        'score',
        'pub_date',
        'title')
    list_filter = ('pub_date', 'author', 'score')
    search_fields = ('text',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Администрирование Комментариев к отзывам на произведения."""

    list_display = (
        'pk',
        'text',
        'author',
        'pub_date',
        'review')
    list_filter = ('pub_date', 'author')
    search_fields = ('text',)
    empty_value_display = '-пусто-'
