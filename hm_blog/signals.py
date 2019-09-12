from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from hm_blog.models import Verification, Follow
from hm_blog.task import password_verification
from hm_blog.task import send_verification_email
from threading import Thread

User = get_user_model()


@receiver(post_save, sender=Follow, dispatch_uid="update_user_following_list")
def update_user_following_list(sender, **kwargs):
   instance = kwargs.get('instance')
   created = kwargs.get('created')
   if created:
       following = Follow.objects.filter(from_user=instance.from_user.following_list)
       id_list = [follow.to_user_id for follow in following]
       instance.from_user.following_list = f"{id_list}"
       instance.from_user.save()


@receiver(post_delete, sender=Follow, dispatch_uid="delete_user_following_list")
def delete_user_following_list(sender, **kwargs):
   instance = kwargs.get('instance')
   created = kwargs.get('created')
   following = Follow.objects.filter(from_user=instance.from_user.following_list)
   id_list = [follow.to_user_id for follow in following]
   instance.from_user.following_list = f"{id_list}"
   instance.from_user.save()


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
        link = f"http://localhost:8008/verify/{obj.token}/{obj.user_id}/"
        background_job = Thread(target=send_verification_email, args=(obj.user.email, link))
        background_job.start()


# @receiver(post_save, sender=Verification, dispatch_uid='send_mail_to_user')
# def send_mail_to_user(*args, **kwargs):
#     obj = kwargs.get("instance")
#     created = kwargs.get("created")
#     if created:
#         if obj.verification_type == 0:
#             link = f"/verify_passw/{obj.token}/{obj.user_id}/"
#             background_job = Thread(target=password_verification, args=(obj.user.email, link))
#             background_job.start()
#         else:
#             link = f"http://localhost:8008/verify/{obj.token}/{obj.user_id}/"
#             background_job = Thread(target=send_verification_email, args=(obj.user.email, link))
#             background_job.start()
