from django.contrib import admin
from .models import Application
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class ApplicationModelAdmin(admin.ModelAdmin):
    list_display = ['tutor_name', 'student_name',
                    'status', 'applied_at', 'cancel']
    list_filter = ['status', 'cancel', 'applied_at']
    search_fields = ['student__user__first_name', 'tutor__user__first_name']

    def student_name(self, obj):
        return obj.student.get_full_name()
    student_name.short_description = 'Student Name'

    def tutor_name(self, obj):
        return obj.tutor.user.get_full_name()
    tutor_name.short_description = 'Tutor Name'

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.status == 'accepted':
            email_subject = "Your Application is Accepted"
            email_body = render_to_string('admin_email.html', {
                'student': obj.student.user
            })
            email = EmailMultiAlternatives(
                email_subject,
                '',
                to=[obj.student.user.email]
            )
            email.attach_alternative(email_body, "text/html")
            email.send()


admin.site.register(Application, ApplicationModelAdmin)
