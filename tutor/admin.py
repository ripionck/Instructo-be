from django.contrib import admin
from .models import Tutor, Review, SubjectChoice


class TutorModelAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'tuition_class',
        'availability',
        'medium',
        'student_gender',
        'tutor_gender',
        'number_of_students',
        'tutoring_experience',
        'salary',
        'location'
    )
    list_filter = ('tuition_class', 'availability', 'medium')
    search_fields = ('title', 'description', 'location')


admin.site.register(Tutor, TutorModelAdmin)
admin.site.register(Review)
admin.site.register(SubjectChoice)
