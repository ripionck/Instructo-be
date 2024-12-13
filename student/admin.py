from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'mobile', 'image']
    search_fields = ['user__first_name', 'user__last_name', 'mobile']
    list_filter = ['gender', 'medium_of_instruction', 'current_class']

    def first_name(self, obj):
        return obj.user.first_name
    first_name.admin_order_field = 'user__first_name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.admin_order_field = 'user__last_name'
