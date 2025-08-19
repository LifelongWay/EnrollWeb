from django.db import models
from departments.models import Department
# Create your models here.
class Course(models.Model):
    # department related
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank = False,
        null = False,
        related_name= 'courses'
        )

    # recommended primary key
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 20, blank = False)
    credits = models.IntegerField()
    prerequisite_courses = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank = True,
        related_name = 'prerequisites'
        )

class Section(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    SEMESTER_CHOICES = [
        ('spring', 'Spring'),
        ('fall', 'Fall'),
        ('summer', 'Summer')
    ]

    section_number = models.IntegerField(blank = False, null = False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name= 'sections')
    capacity = models.PositiveSmallIntegerField(default = 0)
    year = models.IntegerField(blank = False, null = False)    
    semester = models.CharField(choices=SEMESTER_CHOICES, blank = False, null = False)
    
    class Meta:
        unique_together = ('course', 'section_number', 'year', 'semester')
