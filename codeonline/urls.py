from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'online_request_list/$',views.online_request_list,name='online_request_list' ),
    url(r'update_request_api/$',views.update_request_api,name='update_request_api' ),
    url(r'dashboard/$',views.dashboard,name='dashboard' ),
    url(r'get_reqest_list_json_api/$',views.get_reqest_list_json_api,name='get_reqest_list_json_api'),

]
