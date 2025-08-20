from django.shortcuts import render
from .models import Course
# Create your views here.
def courses_and_sections_view(request):
    courses = Course.objects.all()
    return render(request ,'courses/courses_panel.html', {'courses': courses})