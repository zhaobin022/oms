# -*- coding: UTF-8 -*-
from django.shortcuts import render,HttpResponse,render_to_response
from api.saltapi import SaltAPI
import json
import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from cmdb import models as cmdb_models
from user_center import forms
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
# Create your views here.



def custom_404(request):
    return render_to_response('404.html')


def login(request):
    if request.method == 'GET':
        form = forms.UserLoginForm()
        return render(request, 'user_center/login.html', {'form':form})
    else:
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            user_login_form_info = form.clean()
            username = user_login_form_info['username']
            password = user_login_form_info['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')

            else:
                errors = {}
                errors['login'] = [u'用户名或密码错误']

                return render(request, 'user_center/login.html', {'form':form,'errors':errors})
        else:
            errors = form.errors
            return render(request, 'user_center/login.html', {'form':form,'errors':errors})
@login_required
def logout(request):
    request.user
    auth.logout(request)
    return HttpResponseRedirect("/user_center/login/")

@login_required
def reset_password(request):
    if request.method == 'GET':
        form = forms.RestPassword()
        return render(request, 'user_center/reset_password.html', {'form':form})
    else:
        form = forms.RestPassword(request.POST)
        if form.is_valid():
            user_login_form_info = form.clean()
            repassword = user_login_form_info['repassword']
            password = user_login_form_info['password']
            oldpassword = user_login_form_info['oldpassword']
            user = auth.authenticate(username=request.user.username, password=oldpassword)
            errors = {}
            if user is not None and user.is_active:
                if password.strip() == repassword.strip():
                    user = request.user
                    user.set_password(password)
                    user.save()
                    auth.logout(request)
                    errors['successfull'] = [u'''<a href="/user_center/login/">修改密码成功,请重新登录</a>''']

                else:
                    errors['login'] = [u'新密码不一致']

            else:
                errors['login'] = [u'旧密码输入错误']

            return render(request, 'user_center/reset_password.html', {'form':form,'errors':errors})
        else:
            errors = form.errors
            return render(request, 'user_center/reset_password.html', {'form':form,'errors':errors})






