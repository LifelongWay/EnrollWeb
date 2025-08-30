from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.apps import apps
from faker import Faker
import random

from departments.models import Department
from users.models import Teacher, Student, Registrar
from courses.models import Course, Section, Enrollment
from curriculums.models import Program, Curriculum

fake = Faker()

class Command(BaseCommand):
    help = 'Flush and populate DB with realistic data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Flushing all data...")
        # Delete all data in all models
        for model in apps.get_models():
            model.objects.all().delete()
        self.stdout.write("Database cleared!")

        # --- 1. Departments ---
        departments = []
        for name in ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Chemistry']:
            dept, _ = Department.objects.get_or_create(name=name)
            departments.append(dept)

        # --- 2. Users & Teachers ---
        teachers = []
        for _ in range(15):
            username = fake.user_name()
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='password123'
            )
            teacher = Teacher.objects.create(
                user=user,
                department=random.choice(departments)
            )
            teachers.append(teacher)

        # --- 3. Students ---
        students = []
        for _ in range(50):
            username = fake.user_name()
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='password123'
            )
            student = Student.objects.create(
                user=user,
                department=random.choice(departments),
                advisor=random.choice(teachers),
                gpa=round(random.uniform(2.0, 4.0), 2),
                program=None  # will assign later
            )
            students.append(student)

        # --- 4. Programs ---
        programs = []
        for dept in departments:
            for degree, _ in Program.DEGREE_CHOICES:
                program = Program.objects.create(
                    name=f"{dept.name} {degree}",
                    degree=degree,
                    department=dept
                )
                programs.append(program)

        # Assign programs to students
        for student in students:
            student.program = random.choice(programs)
            student.save()

        # --- 5. Courses ---
        courses = []
        for dept in departments:
            for i in range(5):
                course = Course.objects.create(
                    department=dept,
                    name=f"{dept.name[:4]}{100+i}",
                    credits=random.choice([3,4])
                )
                courses.append(course)

        # Add prerequisites randomly
        for course in courses:
            prereqs = random.sample(courses, random.randint(0, 2))
            for prereq in prereqs:
                if prereq != course:
                    course.prerequisite_courses.add(prereq)

        # --- 6. Curriculums ---
        for program in programs:
            program_courses = random.sample(courses, k=min(5, len(courses)))
            for sem, course in enumerate(program_courses, 1):
                Curriculum.objects.create(
                    program=program,
                    course=course,
                    numbered_semester=sem
                )

        # --- 7. Sections ---
        sections = []
        for course in courses:
            for sec_num in range(1, random.randint(2,4)):
                section = Section.objects.create(
                    course=course,
                    teacher=random.choice(teachers),
                    section_number=sec_num,
                    capacity=random.randint(20, 50),
                    semester=random.choice(['spring', 'fall', 'summer']),
                    year=int(fake.year())  # Fix year type
                )
                sections.append(section)

        # --- 8. Enrollments ---
        for student in students:
            student_sections = random.sample(sections, k=random.randint(2,5))
            for section in student_sections:
                Enrollment.objects.create(
                    student=student,
                    section=section,
                    grade=random.choice([g[0] for g in Enrollment.GRADE_CHOICES])
                )

        # --- 9. Registrars ---
        for _ in range(3):
            username = fake.user_name()
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='password123'
            )
            Registrar.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
