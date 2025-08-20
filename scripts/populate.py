import random
from django.contrib.auth.models import User
from datetime import date
from departments.models import Department
from users.models import Teacher, Student
from courses.models import Course, Section, Enrollment


def populate():
    # -----------------------------
    # 1. Departments
    # -----------------------------
    departments_data = ["Computer Science", "Electrical Eng.", "Mechanical Eng.", "Business", "Mathematics"]
    departments = []

    for name in departments_data:
        dept, _ = Department.objects.get_or_create(name=name)
        departments.append(dept)

    # -----------------------------
    # 2. Teachers
    # -----------------------------
    teachers_data = [
        ("Alice", "Smith", "Computer Science"),
        ("Bob", "Johnson", "Electrical Eng."),
        ("Carol", "Williams", "Mechanical Eng."),
        ("David", "Brown", "Business"),
        ("Eva", "Davis", "Mathematics")
    ]

    teachers = []
    for first, last, dept_name in teachers_data:
        user, _ = User.objects.get_or_create(username=f"{first.lower()}.{last.lower()}", first_name=first, last_name=last)
        dept = Department.objects.get(name=dept_name)
        teacher, _ = Teacher.objects.get_or_create(user=user, department=dept)
        teachers.append(teacher)

    # -----------------------------
    # 3. Courses
    # -----------------------------
    courses_data = [
        ("Algorithms", "Computer Science", 4, []),
        ("Data Structures", "Computer Science", 3, []),
        ("Circuits", "Electrical Eng.", 4, []),
        ("Thermodynamics", "Mechanical Eng.", 3, []),
        ("Finance 101", "Business", 3, []),
        ("Linear Algebra", "Mathematics", 4, [])
    ]

    courses = []
    for name, dept_name, credits, prereqs in courses_data:
        dept = Department.objects.get(name=dept_name)
        course, _ = Course.objects.get_or_create(name=name, department=dept, credits=credits)
        # add prerequisites if any
        for pre_name in prereqs:
            pre_course = Course.objects.get(name=pre_name)
            course.prerequisite_courses.add(pre_course)
        courses.append(course)

    # -----------------------------
    # 4. Students
    # -----------------------------
    students_data = [
        ("John", "Doe", "Computer Science", 3.5),
        ("Mary", "Johnson", "Computer Science", 3.8),
        ("Steve", "Williams", "Electrical Eng.", 3.2),
        ("Linda", "Brown", "Mechanical Eng.", 3.0),
        ("James", "Davis", "Business", 3.7),
        ("Patricia", "Miller", "Mathematics", 3.9)
    ]

    students = []
    for first, last, dept_name, gpa in students_data:
        user, _ = User.objects.get_or_create(username=f"{first.lower()}.{last.lower()}", first_name=first, last_name=last)
        dept = Department.objects.get(name=dept_name)
        advisor = random.choice([t for t in teachers if t.department == dept]) if dept else None
        student, _ = Student.objects.get_or_create(user=user, department=dept, advisor=advisor, gpa=gpa)
        students.append(student)

    # -----------------------------
    # 5. Sections
    # -----------------------------
    sections = []
    semesters = ["spring", "fall", "summer"]
    for course in courses:
        for i in range(1, 3):  # 2 sections per course
            teacher = random.choice([t for t in teachers if t.department == course.department])
            year = 2025
            semester = random.choice(semesters)
            section, _ = Section.objects.get_or_create(
                course=course,
                section_number=i,
                teacher=teacher,
                capacity=30,
                year=year,
                semester=semester
            )
            sections.append(section)

    # -----------------------------
    # 6. Enroll Students
    # -----------------------------
    grades = ['AA', 'AB', 'BB', 'BC', 'CC', 'CD', 'DD', 'FF', 'P']

    for student in students:
        # enroll each student in 2-3 sections randomly
        enroll_sections = random.sample(sections, k=random.randint(2, 3))
        for section in enroll_sections:
            Enrollment.objects.get_or_create(
                student=student,
                section=section,
                enrollment_date=date.today(),
                grade=random.choice(grades)
            )

    print("Database population complete!")
