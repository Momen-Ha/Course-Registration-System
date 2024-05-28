
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student

@receiver(post_save, sender=Student)
def create_user_for_student(sender, instance, created, **kwargs):
    if created and instance.user is None:
        user, created = User.objects.get_or_create(
            username=instance.email,
            defaults={'email': instance.email, 'password': instance.password}
        )
        instance.user = user
        instance.save()
