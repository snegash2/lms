from .models import Category
def my_context_processor(request):
    return {
        'categories': Category.objects.all()
    }