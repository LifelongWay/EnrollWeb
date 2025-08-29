from django.shortcuts import render,redirect
from .models import Course, Section
from .forms import CourseForm, SectionForm
from django.db.models import Case, When

from departments.models import Department
# Create your views here.


def courses_and_sections_view(request, course_name = None, course_id = None, type=None):
    # when course_name and course_id are given -> it's section creation
    if course_name and course_id: type = 'section'

    # courses are always in context
    context = {}
    context['courses'] = Course.objects.all()
    context['departments'] = Department.objects.all()

    chosen_department = request.GET.get('department')
    if chosen_department != '' and chosen_department:
        context['courses'] = Course.objects.all().filter(department = chosen_department)
        context['selected_department'] = int(chosen_department)

    if request.method == 'POST':
        # get submitted form
        if type == 'course':
            add_form = CourseForm(request.POST)
        elif type == 'section':
            add_form = SectionForm(request.POST, request.FILES, course = context['courses'].get(pk = course_id))
        
        if add_form.is_valid():
            print("VALID!")
            # add instance
            add_form.save()
        else:
            print(add_form.errors)
        # after querying escape querying url moving to courses page 
        return redirect('courses:panel')
    else:                  # GET
        # getting add form. 
        if type == 'course':
            course_form = CourseForm()
            context['add_course_form'] = course_form
        elif type == 'section':  # getting course edit form
            section_form = SectionForm() 
            context['add_section_form'] = section_form
            # add tp context which course it belongs to
            context['course_id'] = course_id
            context['courses'] = context['courses'].annotate(
                first=Case(
                    When(pk=course_id, then=0),
                    default=1
                )
            ).order_by('first')

    # return courses with form, if gotten
    return render(request ,'courses/courses_panel.html', context)

def courses_and_sections_edit_view(request, type, pk):
    context = {}
    context['courses'] = Course.objects.all()

    if request.method == 'POST':
        if type == 'course':
            pass
        elif type == 'section':
            section_instance = Section.objects.get(pk = pk)
            form = SectionForm(request.POST, request.FILES,  instance = section_instance)
            form.save()
        return redirect('courses:panel')
    else:
        
        if type == 'course':
            old_course = Course.objects.get(pk = pk)
            course_form = CourseForm(instance = old_course)
            context['edit_course_pk'] = pk
            context['edit_course_form'] = course_form
        elif type == 'section':
            old_section = Section.objects.get(pk = pk)
            section_form = SectionForm(instance=old_section)
            context['edit_section_pk'] = pk
            context['edit_section_form'] = section_form
            context['courses'] = context['courses'].annotate(
                first=Case(
                    When(pk=old_section.course.pk, then=0),
                    default=1
                )
            ).order_by('first')
    return render(request, 'courses/courses_panel.html' ,context)

def courses_and_sections_delete_view(request, type, pk):
    if type == 'section':
        # get deleting section
        instance_to_delete = Section.objects.get(pk = pk)
    elif type == 'course':
        # get deleting course
        instance_to_delete = Course.objects.get(pk = pk)
    # delete
    instance_to_delete.delete() 
    return redirect('courses:panel')


# For Teachers and Students

def my_sections_view(request):
    
    # get sections based on user's role
    user = request.user
    sections = {}
    if hasattr(user, 'student'):
        sections = user.student.sections.all()
    elif hasattr(user, 'teacher'):
        sections = user.teacher.sections.all()
    # else {} -- already initialized

    
    # build context
    # context
    context = {
        'sections': sections
    }


    return render(request, 'courses/my_sections.html', context)

