from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class AdminModel(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="admin_profile"
    )
    phone_regex = RegexValidator(
        regex=r'^\+?88[0-9]{11}$',
        message="Phone number must be entered in the format: '+8801234567890'"
    )
    mobile_no = models.CharField(
        validators=[phone_regex],
        max_length=14,
        help_text="Contact phone number in Bangladesh format (+8801XXX)",
        unique=True
    )

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def get_full_name(self):
        return self.__str__()
