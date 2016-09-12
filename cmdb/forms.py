# encoding: utf-8
import re
from django import forms
from django.core.exceptions import ValidationError
import models

def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


def username_validate(value):
    username_re = re.compile(r'^\w+$')
    if not username_re.match(value):
        raise ValidationError('用户格式错误')

class UserLoginForm(forms.Form):
    username = forms.CharField(
        validators=[username_validate,],
        error_messages={'required': u'用户名不能为空',},
        widget=forms.TextInput(
            attrs={
                'id':'username',
                'name': 'username',
                'class': 'form-control',
                'placeholder': u'用户名',
                'required':True,
                'data-toggle':"tooltip",
                "data-placement":"right",
                "data-content":"Vivamus sagittis lacus vel augue laoreet rutrum faucibus."
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




class ExecuteCommandForm(forms.Form):
    # server_list = models.Server.objects.all()
    # server_choice = []
    # for s in server_list:
    #     t = (s.id,"%s(%s)" %  (s.server_name,s.ipaddress))
    #     server_choice.append(t)
    #
    # server_list = forms.MultipleChoiceField(
    #     choices=tuple(server_choice),
    #     widget=forms.widgets.SelectMultiple(
    #         attrs={
    #             'class': 'form-control',
    #             'id': 'server_list',
    #             'size': "10",
    #             'name': '"server_list"'
    #         }
    #     )
    # )
    command = forms.CharField(
        error_messages={'required': u'命令不能为空',},
        widget=forms.TextInput(
            attrs={
                'id':'command',
                'name': 'command',
                'class': 'form-control',
                'placeholder': u'执行命令',
                # 'required':True,
                'type':"text",
            })
    )
                        # <input id="command" name="command" type="text" placeholder="执行命令" class="form-control">



class DeploySoftwareForm(forms.Form):
    # software_list = models.SoftwareList.objects.all()
    # software_choice = []
    # for s in software_list:
    #     t = (s.id,s.software_name)
    #     software_choice.append(t)
    #
    #
    # server_list = models.Server.objects.all()
    # server_choice = []
    # for s in server_list:
    #     t = (s.id,"%s(%s)" %  (s.server_name,s.ipaddress))
    #     server_choice.append(t)
    server_list = forms.MultipleChoiceField(
        # choices=tuple(server_choice),
        widget=forms.widgets.SelectMultiple(
            attrs={
                'class': 'form-control',
                'id': 'server_list',
                'size': "10",
                'name': '"server_list"'
            }
        )
    )

    software_list = forms.MultipleChoiceField(
        # choices=tuple(software_choice),
        widget=forms.widgets.SelectMultiple(
            attrs={
                'class': 'form-control',
                'id': 'software_list',
                'size': "10",
                'name': '"software_list"'
            }
        )
    )



class UpdateCodeForm(forms.Form):
    # app_list_choice = []
    # app_l = models.App.objects.all()
    #
    # for a in app_l:
    #     app_list_choice.append((a.id,a.app_name))
    app_list = forms.MultipleChoiceField(
        # choices=tuple(app_list_choice),
        widget=forms.widgets.SelectMultiple(
            attrs={
                'class': 'form-control',
                'id': 'app_list',
                'size': "10",
                'name': '"app_list"'
            }
        )
    )
    # svn_version = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'id':'svn_version',
    #             'name': 'svn_version',
    #             'class': 'form-control',
    #             'placeholder': u'svn 版本如不输入则更新到最新版本',
    #             'required':False,
    #             'type':"text",
    #         })
    # )