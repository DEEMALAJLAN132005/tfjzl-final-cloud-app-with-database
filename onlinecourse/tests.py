"""Integration tests for the final Django online-course assessment feature."""
from datetime import date

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Course, Enrollment, Question, Submission


class AssessmentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="learner", password="example-only-password"
        )
        cls.course = Course.objects.create(
            name="Learning Django",
            image="course_images/question.png",
            description="Django fundamentals",
            pub_date=date.today(),
        )
        cls.enrollment = Enrollment.objects.create(user=cls.user, course=cls.course)
        cls.question = Question.objects.create(
            course=cls.course, question_text="Is Django a Python framework?", grade=100
        )
        cls.correct = Choice.objects.create(
            question=cls.question, choice_text="Yes", is_correct=True
        )
        cls.incorrect = Choice.objects.create(
            question=cls.question, choice_text="No", is_correct=False
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_grading_rubric_model_fields_and_admin(self):
        """Verify the precise names required by the AI grading rubric."""
        self.assertEqual(
            Question._meta.get_field("question_text").name, "question_text"
        )
        self.assertEqual(
            Choice._meta.get_field("choice_text").name, "choice_text"
        )
        self.assertIn("question_text", admin.site._registry[Question].list_display)
        submission = Submission.objects.create(enrollment=self.enrollment)
        self.assertIn("Submission", str(submission))

    def test_grading_rubric_result_route_name(self):
        submission = Submission.objects.create(enrollment=self.enrollment)
        result_url = reverse(
            "onlinecourse:show_exam_result",
            args=(self.course.pk, submission.pk),
        )
        self.assertIn("/result/", result_url)

    def test_question_requires_exact_correct_choice_set(self):
        self.assertTrue(self.question.is_get_score([self.correct.pk]))
        self.assertFalse(self.question.is_get_score([self.incorrect.pk]))
        self.assertFalse(
            self.question.is_get_score([self.correct.pk, self.incorrect.pk])
        )
        self.assertFalse(self.question.is_get_score([]))

    def test_course_detail_displays_assessment(self):
        url = reverse("onlinecourse:course_details", args=(self.course.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Start Exam")
        self.assertContains(response, "Is Django a Python framework?")
        self.assertContains(response, "Learning Django")

    def test_correct_answers_show_congratulations(self):
        url = reverse("onlinecourse:submit", args=(self.course.pk,))
        response = self.client.post(
            url, {f"choice_{self.correct.pk}": str(self.correct.pk)}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Congratulations")
        self.assertContains(response, "100/100")
        self.assertContains(response, "Correct answer: Yes")
        self.assertEqual(Submission.objects.count(), 1)

    def test_incorrect_answers_show_fail(self):
        url = reverse("onlinecourse:submit", args=(self.course.pk,))
        response = self.client.post(
            url, {f"choice_{self.incorrect.pk}": str(self.incorrect.pk)},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Failed")
        self.assertContains(response, "0/100")
        self.assertContains(response, "Wrong answer: No")

    def test_submit_requires_post(self):
        response = self.client.get(
            reverse("onlinecourse:submit", args=(self.course.pk,))
        )
        self.assertEqual(response.status_code, 405)

    def test_other_learners_cannot_see_submission(self):
        submission = Submission.objects.create(enrollment=self.enrollment)
        other = get_user_model().objects.create_user(
            username="other", password="another-example-only-password"
        )
        self.client.force_login(other)
        response = self.client.get(
            reverse(
                "onlinecourse:show_exam_result",
                args=(self.course.pk, submission.pk),
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_non_enrolled_user_cannot_submit(self):
        other = get_user_model().objects.create_user(
            username="not_enrolled", password="another-example-only-password"
        )
        self.client.force_login(other)
        response = self.client.post(
            reverse("onlinecourse:submit", args=(self.course.pk,)),
            {f"choice_{self.correct.pk}": str(self.correct.pk)},
        )
        self.assertEqual(response.status_code, 404)
