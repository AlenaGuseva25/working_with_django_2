from django.db import models

from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=150,verbose_name='Название курса', blank=False)
    description = models.TextField(verbose_name='Описание курса', blank=False)
    preview = models.ImageField(upload_to='course_previews/', verbose_name='Превью', blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец курса', db_index=True)

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name']


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название урока', blank=False)
    description = models.TextField(verbose_name='Описание урока', blank=False)
    preview = models.ImageField(upload_to='lesson_previews/', blank=False, verbose_name='Превью',)
    link_to_the_video = models.URLField(verbose_name='Ссылка на видео', blank=False)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец урока', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name']
