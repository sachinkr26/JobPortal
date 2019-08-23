from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from erpq.models import documents

# Create your views here.


def index(request):

    return render(request, 'erpq')


def documents(request):
    jobs_list = documents.objects.order_by('birthday')
    paginator = Paginator(jobs_list, 25)
    page_number = request.GET.get('page')
    try:
        user_list = paginator.page(page_number)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        jobs_list = paginator.page(paginator.num_pages)
    return render(request, 'erpq/home.html', {'jobs_list': jobs_list})

