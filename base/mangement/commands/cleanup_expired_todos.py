from django.core.management.base import BaseCommand
from django.utils import timezone
from base.models import Todo

class Command(BaseCommand):
    help = 'Deletes todos that have passed their expiration time'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_todos = Todo.objects.filter(expires_at__lte=now)
        count = expired_todos.count()
        expired_todos.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired todos'))
