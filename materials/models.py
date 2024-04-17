from django.db import models
from config import settings



class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    preview = models.ImageField(upload_to='materials/static/img', verbose_name='изображение', null=True, blank=True)
    description = models.TextField(max_length=250, verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField(default=1000, verbose_name='цена')

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name='курс'
        verbose_name_plural='курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    preview = models.ImageField(upload_to='materials/static/img', verbose_name='изображение', null=True, blank=True)
    description = models.TextField(max_length=250, verbose_name='описание')
    url = models.URLField(max_length=200, verbose_name='ссылка на видео', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='курс', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name='урок'
        verbose_name_plural='уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    status_subscrip = models.BooleanField(default=False, verbose_name='статус подписки')

    def __str__(self):
        return f'{self.course} {self.status_subscrip}'

    class Meta:
        verbose_name='подписка'
        verbose_name_plural='подписки'
