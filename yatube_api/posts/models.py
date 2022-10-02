from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    """Определение модели системы подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    def clean(self):
        if self.user == self.following:
            raise ValidationError('Нельзя подписываться на самого себя.')

    class Meta:
        unique_together = 'user', 'following'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Group(models.Model):
    """Определение модели Group и ее полей."""
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальное обозначение группы',
    )
    description = models.TextField(verbose_name='Описание группы')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        """Вывод названия группы."""
        return self.title
