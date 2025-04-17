from django.core.management.base import BaseCommand
from users.models import Payments
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson

class Command(BaseCommand):
    hepl = 'Заполнение таблицы Payments'

    def handle(self, *args, **options):
        User = get_user_model()

        try:
            user_1 = User.objects.get(email='test@example.com')
            user_2 = User.objects.get(email='test1@example.com')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Необходимо создать пользователей test@example.com и test1@example.com!'))
            return

        try:
            course_1 = Course.objects.get(name='Тестовый курс')
        except Course.DoesNotExist:
            self.stdout.write(self.style.ERROR('Не найден курс "Тестовый курс"!"'))
            return

        try:
            lesson_1 = Lesson.objects.get(name='Тестовый урок')
        except Lesson.DoesNotExist:
            self.stdout.write(self.style.ERROR('Не найден урок "Тестовый урок"!"'))
            return

        Payments.objects.create(user=user_1, course=course_1, amount=100.00, method='cash')
        Payments.objects.create(user=user_2, lesson=lesson_1, amount=100.00, method='transfer')

        self.stdout.write(self.style.SUCCESS('Платежи добавлены'))