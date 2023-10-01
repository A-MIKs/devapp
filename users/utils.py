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

def searchProfiles(request):
    search_query = ""
    profiles = Profile.objects.all()
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
        skill = Skill.objects.filter(name__iexact=search_query)
        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query)| 
            Q(short_intro__icontains=search_query)| 
            Q(skill__in=skill))
    return profiles, search_query