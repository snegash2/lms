from django.dispatch import receiver
from crudbuilder.signals import post_inline_create_signal
from exam.multichoice.models import Multichoice

@receiver(post_inline_create_signal, sender=Multichoice)
def post_inline_create_handler(sender, **kwargs):
    print("request reached here")
     
    parent = kwargs['parent']
    children = kwargs['children']
    parent.save()

    for child in children:
        child.quiz = parent
        child.save()