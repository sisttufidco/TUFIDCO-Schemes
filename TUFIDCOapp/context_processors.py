from .models import scrollModel

def scroll_processor(request):
    scroll = scrollModel.objects.all()
    context = {
        'scroll':scroll,
    }
    return context
