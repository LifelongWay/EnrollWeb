from django.shortcuts import render
from departments.models import Department
# Create your views here.
def curriculums_editor(request):
    context = {}
    context['departments'] = Department.objects.all()

    return render(request, 'curriculums/curriculum_editor.html', context)

def my_curriculum(request):
    pass