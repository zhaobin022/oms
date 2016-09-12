#coding=utf-8
from django import template
register = template.Library()
#
# @register.filter(name='addcss')
# def addcss(field, css):
#     return field.as_widget(attrs={"class":css})


@register.filter()
def is_production_manager(userprofile):
    return True
