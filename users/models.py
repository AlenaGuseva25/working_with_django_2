from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Электронная почта обязательна')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    phone_number = models.CharField(unique=True, max_length=11, null=True, blank=True, verbose_name="Номер телефона")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']


class Payments(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey('materials.Course', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ссылка на оплаченный курс')
    lesson = models.ForeignKey('materials.Lesson', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ссылка на оплаченный урок')
    amount = models.DecimalField(max_length=20, decimal_places=2, max_digits=10, verbose_name='Сумма оплаты')
    method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')
    payment_session_id = models.CharField(max_length=255, blank=True, null=True)
    payment_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'Платеж на сумму {self.payment_date} от {self.user.email}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['payment_date']


MODERATOR_GROUP_NAME = 'Модераторы'