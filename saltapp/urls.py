from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'file_center/$',views.file_center,name='file_center' ),
]
