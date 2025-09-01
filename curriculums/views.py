from django.shortcuts import render, redirect
from departments.models import Department
from .forms import ProgramNameForm
# Create your views here.
def curriculums_editor(request):
    context = {}
    context['departments'] = Department.objects.all()

    return render(request, 'curriculums/curriculum_editor.html', context)

def curriculum_add(request, dept_id):
    context = {}
    context['departments'] = Department.objects.all()
    
    department_modifying = Department.objects.all().get(pk = dept_id)
    print('A')
    if request.method == 'POST':
        program_form = ProgramNameForm(request.POST)
        if program_form.is_valid():
            print('SDF')
            program_instance = program_form.save(commit = False)
            program_instance.department = department_modifying
            program_instance.save()
        else:
            print('Program Form Errors')
            print(program_form.errors)
        redirect('curriculums:editor')
    else:
        context['program_form'] = ProgramNameForm()
        context['dept_id'] = dept_id
    return render(request, 'curriculums/curriculum_editor.html', context)

def curriculum_edit(request, program_id):
    pass

def curriculum_delete(request, program_id):
    pass

def my_curriculum(request):
    pass