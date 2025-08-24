# user/context_processors.py
from management_admin.models import Category

def categories_processor(request):
    return {
        "categories": Category.objects.all()
    }
