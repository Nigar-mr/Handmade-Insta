from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from hm_blog.models import Verification
from hm_blog.task import send_verification_email
from threading import Thread

User = get_user_model()

@receiver(post_save, sender=User, dispatch_uid='create_token')
def create_token(*args, **kwargs):
    obj = kwargs.get("instance")
    created = kwargs.get("created")
    if created:
        Verification.objects.create(
            user=obj
        )


@receiver(post_save, sender=Verification, dispatch_uid='send_mail_to_user')
def send_mail_to_user(*args, **kwargs):
    obj = kwargs.get("instance")
    created = kwargs.get("created")
    if created:
        link = f"http://localhost:8000/verify/{obj.token}/{obj.user_id}/"
        background_job = Thread(target=send_verification_email, args=(obj.user.email, link))
        background_job.start()
