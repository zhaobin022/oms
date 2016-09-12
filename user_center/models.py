# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)

class UserProfileManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )
    # user_group = models.ManyToManyField(UserGroup,blank=True)
    is_active = models.BooleanField(default=True)
    admin_tag = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    alias = models.CharField(max_length=64,blank=True,null=True)
    position_choice = (
        (0,'产品经理'),
        (1,'测试经理'),
        (2,'开发经理'),
        (3,'运维人员'),
        (4,'运维经理'),
        (5,'技术经理'),
        (6,'超级管理员'),
    )
    position = models.SmallIntegerField(choices=position_choice, blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=64,blank=True,null=True)
    description = models.CharField(max_length=20,  blank=True,null=True,verbose_name=u'人员描述')
    group = models.ForeignKey('UserGroup', blank=True,null=True)
    team_member = models.ManyToManyField('UserProfile',blank=True,related_name='team_leader_set')
    friends =  models.ManyToManyField('UserProfile',blank=True,related_name='friends_set')
    header_image = models.CharField(max_length=64,blank=True,null=True)
    def __unicode__(self):
        return self.username

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    class Meta:
        verbose_name = u'系统用户'
        verbose_name_plural = "系统用户"

class UserGroup(models.Model):
    group_name =  models.CharField(max_length=30,unique=True)
    description = models.TextField()
    def __unicode__(self):
        return self.group_name

    class Meta:
        verbose_name = u'系统组'
        verbose_name_plural = "系统组"

