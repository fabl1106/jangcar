from urllib.parse import urlparse

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from drive.models import Drive
from .forms import DriveRegisterForm
# Create your views here.


class Main(ListView):
    model = Drive
    template_name = 'drive/drive_main1.html'

def drive_create(request):

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, '간단한 회원가입 이후 이용가능합니다 :)')
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
        form = DriveRegisterForm(request.POST)
        form.instance.user_id = request.user.id
        # form.connect = request.user.phone
        print("1")
        if form.is_valid():
            print(3)
            form.save()
            print("2")
            # return redirect(instance)
            return redirect('/')
            # return render(request, 'drive/drive_mylist.html')
    else:
        form = DriveRegisterForm()

    return render(request, 'drive/drive_create2.html', {'form':form})

def drive_update(request, pk):
    drive = get_object_or_404(Drive, pk=pk)

    if request.method == "POST":
        form = DriveRegisterForm(request.POST, instance=drive)
        if form.is_valid():
            instance = form.save()
            Drive_list = Drive.objects.filter(user=request.user.id)
            return render(request, 'drive/drive_mylist.html', {'objects': Drive_list})
    else:

        form = DriveRegisterForm(instance=drive)
        return render(request, 'drive/drive_update.html', {'form':form})

def drive_delete(request, pk):

    drive = get_object_or_404(Drive, pk=pk)

    if request.method == "GET":
        drive.delete()
        Drive_list = Drive.objects.filter(user=request.user.id)
        return render(request, 'drive/drive_mylist.html', {'objects': Drive_list} )
    else:
        return render(request, 'drive/drive_detail.html')


def drive_list(request):

    if request.method == "POST":
        queryset = Drive.objects.all()
        departure_key = request.POST.get('departure_key', None)
        arrive_key = request.POST.get('arrive_key', None)
        date_key = request.POST.get('date_key', None)
        print(departure_key)
        print(arrive_key)
        print(date_key)


        departure_area_q = Q(departure_area__icontains=departure_key)
        arrive_area_q = Q(arrive_area__icontains=arrive_key)
        date_q = Q(departure_date__icontains=date_key)

        print(departure_area_q)
        print(arrive_area_q)
        print(date_q)

        if queryset:
            check_plan = get_list_or_404(queryset, departure_area_q & arrive_area_q & date_q )
            return render(request, 'drive/drive_list.html', {'objects':check_plan, 'departure':departure_key, 'arrive':arrive_key, 'date':date_key})

    if request.method == "GET":
        return render(request, 'drive/drive_main.html')


class DriveDetail(DetailView):
    model = Drive
    template_name = 'drive/drive_detail.html'


def drive_mylist(request):
    if not request.user.is_authenticated:
        return render(request, 'drive/drive_mylist.html')
    else:
        Drive_list = Drive.objects.filter(user=request.user.id)
        if not Drive_list:
            return render(request, 'drive/drive_mylist.html')

        return render(request, 'drive/drive_mylist.html', {'objects': Drive_list})


class MyDriveList(ListView):
    model = Drive
    template_name = 'drive/drive_mylist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = Drive.objects.filter(user=self.request.user.id)
        return context