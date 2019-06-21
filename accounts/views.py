from urllib.parse import urlparse

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.views.generic.base import View

from accounts import *

from .forms import SignUpForm


def signupbefore(request):
    if request.method == "GET":
        return render(request, 'accounts/signup_before.html')


def signup(request):
    if request.method == 'POST':
        # todo : 입력 받은 내용을 이용해서 회원 객체 생성
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            user_instance = signup_form.save(commit=False)
            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.save()
            return render(request, 'accounts/signup_complete.html', {'username':user_instance.username})
        else:
            messages.warning(request, '비밀번호 입력이 일치하지 않습니다')
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

    else:
        # todo: from 객체를 만들어서 전달.
        signup_form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': signup_form.as_p() })