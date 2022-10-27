from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import validate_year

STR_LEN = 15


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название категории',
        help_text='Не более 200 символов'
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Адрес'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Category {self.name}, slug {self.slug}'


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название жанра',
        help_text='Не более 200 символов'
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Адрес'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:STR_LEN]


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название произведения',
        help_text='Не более 200 символов'
    )
    year = models.PositiveSmallIntegerField(
        validators=[validate_year, ],
        verbose_name='Год выпуска произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Описание',
        help_text='Не более 255 символов'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:STR_LEN]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Напишите отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=5,
        validators=[
            MaxValueValidator(
                10,
                message='Оценка не должна быть выше 10'
            ),
            MinValueValidator(
                1,
                message='Оценка не должна быть меньше 1'
            )
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:STR_LEN]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Напишите комментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'

    def __str__(self):
        return self.text[:STR_LEN]
