from django.core.mail import send_mail
from .models import Course,CourseAccess,Category
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import user_logged_in,user_logged_out
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group,Permission

User = get_user_model()

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




@receiver(user_logged_in, sender=User)
def user_logged_in_handler(sender, user, request, **kwargs):
    request.session['is_loading'] = True





# @receiver(post_save, sender=Course)
# def create_group_for_student_to_take_exam(sender, instance, created,**kwargs):
#     group = None
#     if instance.published == False:
#         try:
#             group = CourseAccess.objects.get( name = f"{instance.name} students access group")
#         except CourseAccess.DoesNotExist:
#             pass
        
#         if group:
#              group.user_set.add(instance.teacher)
#              group.course = instance
#              group.save()
             
#         else:
#             group.name = f"{instance.name} students access group"
#             group.course = instance
#             group.save()
        
        
        

@receiver(post_save, sender=Course)
def insert_course_to_specific_category(sender, instance, created,**kwargs):
    category = None
    if created:
        try:
            category = Category.objects.get( category = instance.category)
            category.courses.add(instance)
        except Category.DoesNotExist:
            pass
        
        
        print("category ",category)
   