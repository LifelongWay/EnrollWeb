from django.db import models

# Create your models here.
class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 20, unique = True, blank = False, null = False)