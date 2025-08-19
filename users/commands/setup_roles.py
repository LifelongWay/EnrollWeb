from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    # description of command emerging in $ python3 manage.py help
    help = 'Create initial groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Create groups if not created
        admin_group, _ = Group.objects.get_or_create(name = "Admin")
        teacher_group, _ = Group.objects.get_or_create(name = "Teacher")

        # get courses.Section permissions
        self_assign_to_section = Permission.objects.get(codename = 'assign_self_to_section')
        student_assign_to_section = Permission.object.get(codename = 'assign_student_to_section')

        # assign permissions to groups
        admin_group.permissions.add(self_assign_to_section)
        admin_group.permissions.add(student_assign_to_section)

        teacher_group.permissions.add(self_assign_to_section)

        self.stdout.write(self.style.SUCCESS('Groups and permissions set up successfully.'))
        