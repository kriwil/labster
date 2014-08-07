from django.test import TestCase

from labster.models import UserAttempt
from labster.tests.factories import (
    UserFactory, LabFactory, UserAttemptFactory, create_lab_proxy,
)


class UserAttemptTest(TestCase):

    def setUp(self):
        lab = LabFactory()
        self.lab_proxy = create_lab_proxy(lab=lab)
        self.user = UserFactory()

    def test_get_for_user(self):
        first_user_attempt = UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy)
        second_user_attempt = UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy)

        user_attempt = UserAttempt.objects.latest_for_user(self.lab_proxy, self.user)
        self.assertEqual(second_user_attempt.id, user_attempt.id)
        self.assertNotEqual(first_user_attempt.id, user_attempt.id)

    def test_get_for_user_empty(self):
        user_attempt = UserAttempt.objects.latest_for_user(self.lab_proxy, self.user)
        self.assertIsNone(user_attempt)

    def test_mark_finished(self):
        user_attempt = UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy)
        user_attempt.mark_finished()

        user_attempt = UserAttempt.objects.get(id=user_attempt.id)
        self.assertTrue(user_attempt.is_finished)

    def test_get_total_play_count(self):
        [UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy) for i in range(10)]
        user_attempt = UserAttempt.objects.latest_for_user(self.lab_proxy, self.user)
        self.assertIsNotNone(user_attempt)
        self.assertEqual(user_attempt.get_total_play_count(), 10)
