from django.test import TestCase
from django.urls import reverse, resolve
from users.models import User
from django.test import override_settings

class ProfileSecurityTests(TestCase):
    """testing change password and deleting account"""

    def setUp(self):
        self.user = User.objects.create(username='jack', email='jack@email.com', password='testpassword')
        self.client.login(username='jack@email.com', password='testpassword')

        self.url = reverse('ideas:profile_security', kwargs={'slug':self.user.author.slug})    

    def test_profile_security_success_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_change_password_form(self):
        response = self.client.get(self.url)

        # check for change password form
        self.assertContains(response, '<form method="post">')

        # check for the three password input fields
        self.assertContains(response, '<input type="password" name="old_password"')
        self.assertContains(response, '<input type="password" name="new_password1"')
        self.assertContains(response, '<input type="password" name="new_password2"')

        # check for form submit button
        self.assertContains(response, '<button class="btn btn-primary" type="submit">Save</button>')

    def test_delete_account(self):
        pass
        # check for delete account form
        # self.assertContains(response, '')