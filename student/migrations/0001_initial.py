# Generated by Django 5.1.4 on 2024-12-13 22:12

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Upload student photo', upload_to='student/images/')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+8801234567890'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('tuition_district', models.CharField(blank=True, max_length=100, null=True)),
                ('school', models.CharField(blank=True, max_length=500, null=True)),
                ('group', models.CharField(blank=True, max_length=50, null=True)),
                ('medium_of_instruction', models.CharField(blank=True, choices=[('bangla', 'Bangla Medium'), ('english', 'English Version')], max_length=20, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
    ]
