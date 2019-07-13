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
    template_name = 'drive/drive_main.html'

    # 해당 class형 뷰에서 get_context_data를 통해서 원하는 자료만을 넘겨주도록 설정
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Drive.objects.all().order_by('-pk')[:5]
        return context




def drive_create(request):

    if request.method == "POST":
        # 로그인이 안되어 있으면
        if not request.user.is_authenticated:
            messages.warning(request, '간단한 회원가입 이후 이용가능합니다 :)')
            # 이전 url로 다시 이동하도록 하기
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
        form = DriveRegisterForm(request.POST)
        # print(request.user.id)

        # form에 생성되는 user_id를 요청한 user.id와 동일하도록 한다.
        form.instance.user_id = request.user.id
        if form.is_valid():
            form.save()
            # 해당 drive_list에서 요청한 user가 작성한 것만 filter해와서 render
            Drive_list = Drive.objects.filter(user=request.user.id)
            return render(request, 'drive/drive_mylist.html', {'objects': Drive_list})
        else:
            # 만약에 폼이 다 안채워졌다면 message 송출
            messages.warning(request, '모든 항목을 다 추가해주세요:)')
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
    else:
        # get으로 요청이 올 때는 form만 만들어서 송부해준다.
        form = DriveRegisterForm()

    return render(request, 'drive/drive_create.html', {'form':form})

def drive_update(request, pk):
    # 해당 요청온 pk의 값을 받아서 drive에 넣어서
    drive = get_object_or_404(Drive, pk=pk)
    if request.method == "POST":
        form = DriveRegisterForm(request.POST, instance=drive)
        form.instance.user_id = request.user.id
        if form.is_valid():
            form.save()
            # drive = form.save()
            Drive_list = Drive.objects.filter(user=request.user.id)
            return render(request, 'drive/drive_mylist.html', {'objects': Drive_list})
    else:
        # get형태로 오면 기존에 instance에 drive를 넣어서 form을 반환
        form = DriveRegisterForm(instance=drive)
        return render(request, 'drive/drive_update.html', {'form':form, 'object':drive})

def drive_delete(request, pk):
    drive = get_object_or_404(Drive, pk=pk)

    if request.method == "GET":
        # get요청으로 오면 그냥 바로 지운다.
        drive.delete()
        Drive_list = Drive.objects.filter(user=request.user.id)
        return render(request, 'drive/drive_mylist.html', {'objects': Drive_list} )
    else:
        return render(request, 'drive/drive_detail.html')


def drive_list(request):

    if request.method == "POST":
        # 등록된 최신순으로 나올 수 있도록 변경. 추후에 시간의 역순으로 나올 수 있도록 해주고 싶다.
        queryset = Drive.objects.all().order_by('-pk')
        departure_key = request.POST.get('departure_key', None)
        arrive_key = request.POST.get('arrive_key', None)
        date_key = request.POST.get('date_key', None)

        departure_area_q = Q(departure_area__icontains=departure_key)
        arrive_area_q = Q(arrive_area__icontains=arrive_key)
        date_q = Q(departure_date__icontains=date_key)

        if queryset:
            check_plan = get_list_or_404(queryset, departure_area_q & arrive_area_q & date_q )
            return render(request, 'drive/drive_list.html', {'object_list':check_plan, 'departure':departure_key, 'arrive':arrive_key, 'date':date_key})

    if request.method == "GET":
        return render(request, 'drive/drive_main.html')


class DriveDetail(DetailView):
    model = Drive
    template_name = 'drive/drive_detail.html'


def drive_mylist(request):
    # 로그인이 안되어있으면, 그냥 창 띄어주기
    if not request.user.is_authenticated:
        return render(request, 'drive/drive_mylist.html')
    else:
        Drive_list = Drive.objects.filter(user=request.user.id)
        if not Drive_list:
            return render(request, 'drive/drive_mylist.html')

        return render(request, 'drive/drive_mylist.html', {'object_list': Drive_list})


# class MyDriveList(ListView):
#     model = Drive
#     template_name = 'drive/drive_mylist.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['objects'] = Drive.objects.filter(user=self.request.user.id)
#         return context