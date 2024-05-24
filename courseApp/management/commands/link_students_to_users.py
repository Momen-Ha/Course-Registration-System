# your_app/management/commands/link_students_to_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courseApp.models import Student

class Command(BaseCommand):
    help = 'Link all students to users'

    def handle(self, *args, **kwargs):
        students = Student.objects.filter(user__isnull=True)
        for student in students:
            user, created = User.objects.get_or_create(
                username=student.email,
                defaults={'email': student.email, 'password': student.password}
            )
            student.user = user
            student.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully linked student {student.name} to user {user.username}'))
