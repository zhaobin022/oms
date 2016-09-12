from django.contrib import admin
from kombu.transport.django import models as kombu_models
admin.site.register(kombu_models.Message)

# Register your models here.
