from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from core.constrains import GENDER_CHOICES, MEDIUM_OF_INSTRUCTION_CHOICES


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    image = models.ImageField(
        upload_to='student/images/',
        help_text='Upload student photo'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+8801234567890'. Up to 15 digits allowed."
    )
    mobile = models.CharField(
        validators=[phone_regex],
        max_length=15,
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    tuition_district = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    school = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    group = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    medium_of_instruction = models.CharField(
        max_length=20,
        choices=MEDIUM_OF_INSTRUCTION_CHOICES,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def get_full_name(self):
        return self.__str__()
