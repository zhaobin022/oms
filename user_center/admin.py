# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from user_center import models
from models import UserProfile
from models import UserGroup
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from models import UserProfile,UserGroup


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('username', 'password','alias','description','group','team_member','friends', 'is_active', 'is_admin','email')


    # description = models.CharField(max_length=20,  blank=True,null=True,verbose_name=u'人员描述')
    # group = models.ForeignKey('UserGroup', blank=True,null=True)
    # team_member = models.ManyToManyField('UserProfile',blank=True,related_name='team_leader_set')
    #
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','alias','position', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password','alias','position','description','group','team_member','friends', 'header_image','is_active','admin_tag','email','phone',)}),
        ('Permissions', {'fields': ('is_admin','user_permissions',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('team_member','friends',)
# class UserInline(admin.TabularInline):
#     model = UserProfile
#     readonly_fields = ['password','last_login']
#
# class UserGroupAdmin(admin.ModelAdmin):
#     inlines = [UserInline,]


class UserGroupAdmin(admin.ModelAdmin):
    readonly_fields = ['group_name',]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserGroup,UserGroupAdmin)
admin.site.unregister(Group)