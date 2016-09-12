from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'client/config/(\d+)/$',views.client_configs ),
    url(r'client/service/report/$',views.service_data_report ),
    url(r'display_chart/$',views.display_chart , name='display_chart'),
    url(r'monited_host/$',views.monited_host , name='monited_host'),
    url(r'get_latest/$',views.get_latest,name='get_latest'),
]
