from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate(request, queryset, results):
    page = request.GET.get("page")
    paginator = Paginator(queryset, results)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        queryset = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        queryset = paginator.page(page)
    leftIndex = int(page)-1 if (int(page)-1>1) else 1
    rightIndex = int(page)+2 if int(page)+2 <= paginator.num_pages else paginator.num_pages+1
    custom_range = range(leftIndex, rightIndex)

    return custom_range, queryset

def searchProjects(request):
    search_query = ""
    projects = Project.objects.all()
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
        tags = Tag.objects.filter(name__iexact=search_query)
        projects = Project.objects.distinct().filter(Q(title__icontains=search_query) | 
                                          Q(description__icontains=search_query) | 
                                          Q(owner__name__icontains=search_query) |
                                          Q(tags__in= tags))
    return projects, search_query 