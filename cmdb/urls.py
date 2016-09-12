from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'host_list/$',views.index,name='cmdb_host_list' ),
    url(r'remote_execute_command/$',views.cmdb_exe_command,name='cmdb_exe_command' ),
    url(r'deploy_software/$',views.deploy_software,name='deploy_software' ),
    url(r'update_code/$',views.update_code,name='update_code' ),
    url(r'update_server_password/$',views.update_server_password,name='update_server_password' ),
    url(r'update_server_info/$',views.update_server_info,name='update_server_info' ),
    url(r'export_execel/$',views.export_execel,name='export_execel' ),
    url(r'gen_jumpserver_mark/$',views.gen_jumpserver_mark,name='gen_jumpserver_mark' ),
    url(r'gen_salt_config/$',views.gen_salt_config,name='gen_salt_config' ),
]
