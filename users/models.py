from django.db import models
from django.contrib.auth.models import User, Group
from departments.models import Department
# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'teachers')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name= 'teachers')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # save teacher

        # get teacher group
        teacher_group = Group.objects.get_or_create(name = 'teacher') 

    """ note:
        if department is deleted, teacher gets deleted, but user that
        corresponds to this teacher role is not deleted.
        This design has advantage, because user can get role teacher in
        another department without recreating its user account !    
    """

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    gpa = models.FloatField(null = False)

    # ISA rel
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= 'student')
    # studies_in rel
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null = False, blank = False, related_name = 'advised_students')
    # advised_by rel
    advisor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null = True, related_name = 'advised_students')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # save student

        # automatically set corresponding group. (made for permissions handler)
        student_group, _ = Group.objects.get_or_create(name = 'Student')
        self.user.groups.add(student_group) # add group to created student


