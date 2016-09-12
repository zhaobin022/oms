from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'dashboard/$',views.dashboard,name="web_dashboard"),
    url(r'get_contact_list/$',views.get_contact_list,name="get_contact_list"),
    url(r'send_msg/$',views.send_msg,name="send_msg"),
    url(r'get_msg/$',views.get_msg,name="get_msg"),
    url(r'test/$',views.test,name="testtttttttttttt"),
]
