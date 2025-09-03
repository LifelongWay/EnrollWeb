from django import template
from ..models import Curriculum

register = template.Library()

@register.simple_tag
def semesters_in_program(program):
    """
    Returns a sorted list of unique semester numbers for a program.
    """
    semesters = Curriculum.objects.filter(program=program).values_list('numbered_semester', flat=True).distinct()
    if not semesters:
        return []

    min_sem = min(semesters)
    max_sem = max(semesters)

    return list(range(min_sem, max_sem + 1))

@register.simple_tag
def courses_for_semester(program, semester):
    """
    Returns all courses of a program for a given semester.
    """
    curriculums = Curriculum.objects.filter(program=program, numbered_semester=semester)
    return [c.course for c in curriculums]
    