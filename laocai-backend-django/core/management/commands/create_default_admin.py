from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile

class Command(BaseCommand):
    help = 'Create default admin: admin/admin123 and viewer: viewer/viewer123'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            u = User.objects.create_superuser('admin','admin@example.com','admin123')
            UserProfile.objects.create(user=u, role='admin', unit='Sở Xây dựng')
            self.stdout.write(self.style.SUCCESS('Created admin / admin123'))
        if not User.objects.filter(username='viewer').exists():
            v = User.objects.create_user('viewer','viewer@example.com','viewer123')
            UserProfile.objects.create(user=v, role='viewer', unit='')
            self.stdout.write(self.style.SUCCESS('Created viewer / viewer123'))
