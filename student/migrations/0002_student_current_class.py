# Generated by Django 5.1.4 on 2024-12-13 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='current_class',
            field=models.CharField(blank=True, choices=[('class_1', 'Class 1'), ('class_2', 'Class 2'), ('class_3', 'Class 3'), ('class_4', 'Class 4'), ('class_5', 'Class 5'), ('class_6', 'Class 6'), ('class_7', 'Class 7'), ('class_8', 'Class 8'), ('class_9', 'Class 9'), ('class_10', 'Class 10'), ('hsc_1', 'HSC 1st Year'), ('hsc_2', 'HSC 2nd Year')], max_length=20, null=True),
        ),
    ]