import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from labster.forms import UserSaveForm
from labster.models import UserSave
from labster.tests.factories import UserFactory, LabFactory, LabProxyFactory


class UserSaveFormTest(unittest.TestCase):

    def test_new_instance(self):
        lab_proxy = LabProxyFactory(lab=LabFactory())
        user = UserFactory(is_superuser=True)

        file_name = "testfile.txt"
        file_content = b"test content"

        post_data = {}
        file_data = {
            'save_file': SimpleUploadedFile(file_name, file_content),
        }

        form = UserSaveForm(post_data, file_data,
                            user_id=user.id, lab_proxy_id=lab_proxy.id)
        self.assertTrue(form.is_valid())

        user_save = form.save()
        self.assertEqual(user_save.user, user)
        self.assertEqual(user_save.lab_proxy, lab_proxy)

    def test_old_instance(self):
        lab_proxy = LabProxyFactory(lab=LabFactory())
        user = UserFactory(is_superuser=True)
        old_user_save = UserSave.objects.create(user=user, lab_proxy=lab_proxy)

        file_name = "testfile.txt"
        file_content = b"test content"

        post_data = {}
        file_data = {
            'save_file': SimpleUploadedFile(file_name, file_content),
        }

        form = UserSaveForm(post_data, file_data,
                            user_id=user.id, lab_proxy_id=lab_proxy.id)
        self.assertTrue(form.is_valid())

        user_save = form.save()
        self.assertEqual(old_user_save, user_save)
        self.assertEqual(old_user_save.user, user_save.user)
        self.assertEqual(old_user_save.lab_proxy, user_save.lab_proxy)
