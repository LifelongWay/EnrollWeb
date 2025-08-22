from django.db import models
from departments.models import Department
from users.models import Student, Teacher
from django.utils import timezone
# Create your models here.
class Course(models.Model):
    # relationship "dept course"
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
    # relationship "prerequisite"
    prerequisite_courses = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank = True,
        related_name = 'prerequisites'
        )
    
    def __str__(self):
        return f'{self.name}'

class Section(models.Model):
    # relationship "teaches"
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes', null = False, blank = False)
    image = models.ImageField(upload_to='course_images/', blank = True, null = True)

    SEMESTER_CHOICES = [
        ('spring', 'Spring'),
        ('fall', 'Fall'),
        ('summer', 'Summer')
    ]

    section_number = models.IntegerField(blank = False, null = False)

    # weak relationship "course_sec"
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name= 'sections')
    capacity = models.PositiveSmallIntegerField(default = 0)
    year = models.IntegerField(blank = False, null = False, default = timezone.now().year)    
    semester = models.CharField(choices=SEMESTER_CHOICES, blank = False, null = False)
    
    # relationship "enrolls"
    students = models.ManyToManyField(Student, through = "Enrollment", related_name= 'sections')

    class Meta:
        unique_together = ('course', 'section_number', 'year', 'semester')
    
    def __str__(self):
        return f'{self.course.name}.{self.section_number}'
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank = False, null = False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank = False, null = False)
    enrollment_date = models.DateField(default = timezone.now)
    
    GRADE_CHOICES = [
    ('AA', 'AA'),
    ('AB', 'AB'),
    ('BB', 'BB'),
    ('BC', 'BC'),
    ('CC', 'CC'),
    ('CD', 'CD'),
    ('DD', 'DD'),
    ('FF', 'FF'),
    ('P',  'Pending'),
    ]
    grade = models.CharField(choices = GRADE_CHOICES, blank = True, null = False, default= 'P')

    class Meta:
        unique_together = ('student', 'section')