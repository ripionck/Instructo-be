from django.db import models
from core.constrains import CLASS_CHOICES, GENDER_CHOICES, MEDIUM_OF_INSTRUCTION_CHOICES, STAR_CHOICES, SUBJECT_CHOICES, TIME_CHOICES
from student.models import Student
from admin_pannel.models import AdminModel


class SubjectChoice(models.Model):
    name = models.CharField(
        max_length=50,
        choices=SUBJECT_CHOICES
    )

    def __str__(self):
        return self.get_name_display()


class Tutor(models.Model):
    author = models.ForeignKey(
        AdminModel,
        on_delete=models.CASCADE,
        related_name='tuitions',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=100)
    subjects = models.ManyToManyField(
        SubjectChoice,
        related_name='tuitions',
        blank=True
    )
    tuition_class = models.CharField(
        max_length=50,
        choices=CLASS_CHOICES,
        null=True,
        blank=True
    )
    availability = models.BooleanField(
        default=True,
        help_text="Availability status of the tuition"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Detailed Description of the tuition"
    )
    medium = models.CharField(
        max_length=50,
        choices=MEDIUM_OF_INSTRUCTION_CHOICES,
        null=True,
        blank=True,
        help_text="Medium of instruction"
    )
    student_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    tutor_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        help_text="Preferred gender of tutor"
    )
    tutoring_time = models.CharField(
        max_length=20,
        choices=TIME_CHOICES,
        null=True,
        blank=True,
        help_text="Time for tutoring"
    )
    number_of_students = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Salary offered per month",
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    tutoring_experience = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Review(models.Model):
    reviewer = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(
        max_length=10,
        choices=STAR_CHOICES
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Review by {self.reviewer.get_full_name()} for {self.tutor.title}'
