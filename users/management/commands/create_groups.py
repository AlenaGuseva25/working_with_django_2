from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import MODERATOR_GROUP_NAME


class Command(BaseCommand):
    help = 'Создание группы Модераторы'

    def handle(self, *args, **options):
        moderator_group, created = Group.objects.get_or_create(name=MODERATOR_GROUP_NAME)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{MODERATOR_GROUP_NAME}" создана.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{MODERATOR_GROUP_NAME}" уже существует.'))