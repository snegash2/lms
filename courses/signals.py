from django.core.mail import send_mail
from .models import Course
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Course)
def send_new_email(sender, instance, created,**kwargs):
    if instance.published == False:
        print("signals is called")
    #     message = f"sorry your {instance.course_name} is unpublished because of {instance. reason_not_published}"
    #     send_mail(
    #         subject = "email cuz the course status is changed",
    #         from_email="tinsingjobs2k@gmail.com",
    #         recipient_list=[instance.teacher.email,'soffonisol@gmail.com'],
    #         message=message,
    #         fail_silently=False
    #     )

    # else:
    #     message = f"you're {instance.course_name}  has beeen published"
    #     send_mail(
    #         subject = "course ",
    #         from_email="tinsingjobs2k@gmail.com",
    #         recipient_list=[instance.teacher.email,'soffonisol@gmail.com'],
    #         message=message,
    #         fail_silently=False
    #     )

