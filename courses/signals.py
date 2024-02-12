from django.core.mail import send_mail
from .models import Course,CourseAccess,Category
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import user_logged_in,user_logged_out
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group,Permission
from students.models import GlobalSetting
from exam.quiz.models import Quiz
from exam.multichoice.models import MCQuestion


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





@receiver(post_save, sender=Course)
def create_group_for_student_to_take_exam(sender, instance, created,**kwargs):
    if CourseAccess.objects.filter(course = instance).exists():
        pass
    else:
      CourseAccess.objects.create(name = f"{instance} groups",course = instance)
  
        

@receiver(post_save, sender=Course)
def insert_course_to_specific_category(sender, instance, created,**kwargs):
    category = None
    if created:
        try:
            category = Category.objects.get( category = instance.category)
            category.courses.add(instance)
        except Category.DoesNotExist:
            pass





@receiver(post_save, sender=Course)
def create_quiz_when_course_created(sender, instance, created,**kwargs):
    category = None
    if created:
        quiz = Quiz.objects.create(
            course = instance,
            title = f"quiz of course {instance.slug}",
            description = f"""
                    Exam Details:
                    1. Answer the following questions to the best of your ability.

                    2. The exam consists of 3 true/false questions and 5 multiple-choice questions.
                                
            """,
            url = instance.slug,
            random_order = True,
            max_questions = 100,
            answers_at_end = True,
            pass_mark = 50,
            success_text = f"""
            well done 
            """,
            fail_text = f"""
            failed
            
            """,
            draft = True
        )
   

@receiver(post_save, sender=User)
def create_global_setting_when_user_is_create(sender, instance, created,**kwargs):
    global_setting = None
    if created:
        try:
            global_setting = GlobalSetting.objects.create(user = instance,data_stored = {"key": "", "value": ""})
        
        except GlobalSetting.DoesNotExist:
            pass
        
        
        print("global_setting  ",global_setting)
        
        
        

# @receiver(post_save, sender=MCQuestion)
# def automatically_insert_question_to_quiz(sender, instance,created,**kwargs):
 
#     if created:
        
#         quizes = Quiz.objects.all()
#         for quiz in quizes:
#             quiz.questions.set(instance)
#             quiz.save()
#         print("kwargs ",kwargs)
        
        
        
