from django.db import migrations

def create_initial_departments(apps, schema_editor):
    Department = apps.get_model('accounts', 'Department')
    departments = [
        'Computer Science',
        'Electrical Engineering',
        'Mechanical Engineering',
        'Civil Engineering',
        'Business Administration',
        'Economics',
        'Mathematics',
        'Physics',
    ]
    for dept_name in departments:
        Department.objects.create(name=dept_name)

def reverse_initial_departments(apps, schema_editor):
    Department = apps.get_model('accounts', 'Department')
    Department.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_departments, reverse_initial_departments),
    ] 