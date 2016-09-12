from django.contrib import admin
from models import OnlineRequest
# Register your models here.


class OnlineRequestAdmin(admin.ModelAdmin):
     filter_horizontal = (
          'developer',
          'require_side',
          'app',
          'technical_man_fun_confirm_online',
          'product_man_confirm_before_online',
          'test_confirm_before_online',
          'white_box_test',
          'maintenance_persion_comfirm',
          'maintenance_manager_comfirm',
          'test_confirm_after_online',
          'product_man_confirm_after_online',
          'test_man_confirm_after_online',
     )


admin.site.register(OnlineRequest,OnlineRequestAdmin)