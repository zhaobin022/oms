# encoding: utf-8
import re
from django import forms
from django.core.exceptions import ValidationError
import models

class UserLoginForm(forms.Form):
    username = forms.CharField(
        error_messages={'required': u'用户名不能为空',},
        widget=forms.TextInput(
            attrs={
                'id':'username',
                'name': 'username',
                'class': 'form-control',
                'placeholder': u'用户名',
                'required':True,
            })
    )
    password = forms.CharField(
        error_messages={'required': u'密码不能为空',},
        widget=forms.PasswordInput(
            attrs={
                'id':'password',
                'name': 'password',
                'class': 'form-control',
                'placeholder': u'密码',
                'required':True,

            })
    )


class RestPassword(forms.Form):
    oldpassword = forms.CharField(
        error_messages={'required': u'旧密码不能为空',},
        widget=forms.PasswordInput(
            attrs={
                'id':'oldpassword',
                'name': 'oldpassword',
                'class': 'form-control',
                'placeholder': u'输入旧密码',
                'required':True,
            })
    )
    password = forms.CharField(
        error_messages={'required': u'新密码不能为空',},
        widget=forms.PasswordInput(
            attrs={
                'id':'password',
                'name': 'password',
                'class': 'form-control',
                'placeholder': u'请输入密码',
                'required':True,

            })
    )
    repassword = forms.CharField(
        error_messages={'required': u'新密码不能为空',},
        widget=forms.PasswordInput(
            attrs={
                'id':'repassword',
                'name': 'repassword',
                'class': 'form-control',
                'placeholder': u'请再次输入密码',
                'required':True,

            })
    )