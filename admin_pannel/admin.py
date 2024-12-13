from django.contrib import admin
from .models import AdminModel


@admin.register(AdminModel)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'mobile_no']
    search_fields = ['user__first_name', 'user__last_name', 'mobile_no']
    list_filter = ['user__date_joined']

    def first_name(self, obj):
        return obj.user.first_name
    first_name.admin_order_field = 'user__first_name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.admin_order_field = 'user__last_name'
