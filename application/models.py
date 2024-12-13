from django.db import models
from student.models import Student
from tutor.models import Tutor

APPLICATION_STATUS = [
    ('applied', 'Applied'),
    ('accepted', 'Accepted')
]


class Application(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS,
        default='applied',
        null=True,
        blank=True
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    cancel = models.BooleanField(
        default=False,
        help_text="Indicates if the application has been cancelled"
    )

    class Meta:
        ordering = ['-applied_at']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return f'{self.student.get_full_name()} applied for {self.tuition.title}'
