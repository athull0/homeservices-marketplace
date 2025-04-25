from .models import Category
from user.models import *
def search_categories(request):
    query = request.GET.get('q', '')
    workers = []

    if query:
        workers = WorkerProfile.objects.filter(categories__name__icontains=query)

    return {'search_query': query, 'search_results': workers}

