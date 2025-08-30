from django.db import models
from departments.models import Department
from courses.models import Course 

# Create your models here.
from django.db import models
from departments.models import Department
from courses.models import Course 

class Program(models.Model):
    DEGREE_CHOICES = [
        ('BS', 'Bachelor of Science (B.S.)'),
        ('MS', 'Master of Science (M.S.)'),
        ('PhD', 'Doctor of Philosophy (Ph.D.)'),
    ]

    name = models.CharField(max_length=200)
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='programs'
    )
    courses = models.ManyToManyField(
        Course,
        through='Curriculum',
        related_name='programs'
    )

    class Meta:
        unique_together = ('name', 'degree')

    def __str__(self):
        return f"{self.name} ({self.get_degree_display()})"


class Curriculum(models.Model):
    program = models.ForeignKey(Program, blank = False, on_delete=models.CASCADE, related_name='curriculums')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curriculums')
    numbered_semester = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.program.name} - {self.course.name} ({self.grade})"
