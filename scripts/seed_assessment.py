"""Create demo-only content for screenshot evidence in GitHub Actions.

The generated random password and database are temporary runner files.
They are not committed to the repository or included in screenshot artifacts.
"""
import json
import os
import secrets
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
import django  # noqa: E402
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from onlinecourse.models import (  # noqa: E402
    Choice, Course, Enrollment, Instructor, Lesson, Question,
)

username = "demo_course_admin"
password = secrets.token_urlsafe(24)
user, _ = get_user_model().objects.get_or_create(username=username)
user.first_name = "Deem"
user.last_name = "Student"
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

instructor, _ = Instructor.objects.get_or_create(
    user=user, defaults={"total_learners": 1}
)
course, _ = Course.objects.get_or_create(
    name="Learning Django",
    defaults={
        "image": "course_images/question.png",
        "description": "Django is a popular Python web framework.",
        "pub_date": date.today(),
        "total_enrollment": 1,
    },
)
course.instructors.add(instructor)
Lesson.objects.get_or_create(
    course=course, title="What is Django", defaults={
        "order": 0,
        "content": "Django is a Python web framework for building web applications.",
    },
)
Enrollment.objects.get_or_create(user=user, course=course)
question, _ = Question.objects.get_or_create(
    course=course, content="Is Django a Python framework?",
    defaults={"grade": 100},
)
correct, _ = Choice.objects.get_or_create(
    question=question, content="Yes", defaults={"is_correct": True},
)
Choice.objects.get_or_create(
    question=question, content="No", defaults={"is_correct": False},
)
credentials_path = "/tmp/onlinecourse-demo-credentials.json"
with open(credentials_path, "w", encoding="utf-8") as file:
    json.dump(
        {"username": username, "password": password,
         "course_id": course.id, "correct_choice_id": correct.id}, file
    )
os.chmod(credentials_path, 0o600)
print("Demo course and temporary test account created.")
