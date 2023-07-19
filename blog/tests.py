import os
from os.path import join

import django
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
django.setup()

from django.test import TestCase, Client
from blog.tasks import send_contact_email

from blog.models import Contact, User, Group, Post


class IndexTest(TestCase):
    def setUp(self):
        # Creating a superuser
        self.admin = User.objects.create_superuser(
            username='admintwo',
            email='admin@example.com',
            password='adminpassword'
        )
        self.admin.save()
        self.client.login(username='admintwo', password='adminpassword')
        self.image_path = join(settings.MEDIA_ROOT, "posts/blog-1.jpg")
        with open(self.image_path, 'rb') as f:
            image_content = f.read()
            self.image = SimpleUploadedFile(self.image_path, image_content, content_type='image/jpeg')

    ###############################
    def tearDown(self):
        Group.objects.filter(title='title',
                             slug='slug-slug',
                             description='The most popular thing is cats'
                             ).delete()

    ###############################
    def test_get_index_page(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_get_about_page(self):
        response = self.client.get('/about/')

        self.assertEqual(response.status_code, 200)

    def test_get_contact_page(self):
        response = self.client.get('/contact/')

        self.assertEqual(response.status_code, 200)

    def test_new_contact(self):
        self.client.post('/contact/', data={
            'name': 'name',
            'email': 'email@gmail.com',
            'phone': '2321413212',
            'user_website': 'https://lol.com',
            'message': 'Hello my name is Dmitro, i wanna enjoy in this city',
        })

        self.assertTrue(
            Contact.objects.filter(message='Hello my name is Dmitro, i wanna enjoy in this city').exists()
        )

    def test_new_index_contact(self):
        self.client.post('/', data={
            'name': 'name',
            'email': 'email@gmail.com',
            'phone': '2321413212',
            'user_website': 'https://lol.com',
            'message': 'Hello my name is Dmitro, i wanna enjoy in this city',
        })

        self.assertTrue(
            Contact.objects.filter(message='Hello my name is Dmitro, i wanna enjoy in this city').exists()
        )

    def test_get_blog_page_caching_timeout(self):
        response = self.client.get('/blog/', allow_caching=True, cache_timeout=10)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<img class="card-img"')

    def test_get_blog_page_caching(self):
        response = self.client.get('/blog/', allow_caching=True)

        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<img class="card-img"')

    def test_admin_create_group(self):
        response = self.client.post('/create-group/', data={
            'title': 'title',
            'slug': 'slug-slug',
            'description': 'The most popular thing is cats'
        }, follow=True)

        self.assertTrue(response.status_code, 200)

        # fields = ['group', 'title', 'text', 'image']

    def test_admin_create_post(self):
        group = Group.objects.create(
            title='title',
            slug='slug-slug',
            description='The most popular thing is cats',
        )
        response = self.client.post('/create-post/', data={
            'group': group,
            'title': 'title',
            'text': 'text',
            'image': self.image
        }, follow=True)

        self.assertContains(response, group.title)

    def test_get_group_posts(self):
        response = self.client.get(f'/group/code-slug/', follow=True)
        self.assertContains(response, 'It is a long established fact that')

    def test_get_single_post(self):
        response = self.client.get('/single/1/')

        self.assertTrue(response.status_code, 200)

    def test_get_single_post_update_version(self):
        group = Group.objects.create(
            title='title',
            slug='slug-slug',
            description='The most popular thing is cats',
        )
        group_id = f'{group.id}'
        self.client.post('/create-post/', data={
            'group': group_id,
            'title': 'title',
            'text': 'text_text_text_text',
            'image': self.image
        }, follow=True)
        self.assertTrue(
            Post.objects.filter(text='text_text_text_text', group=group_id).exists())


class StaffTestCase(TestCase):
    def test_staff_view(self):
        # Create a user if necessary for authentication
        # Create a contact
        contact = Contact.objects.create(
            name='name',
            email='email@gmail.com',
            phone='2321413212',
            user_website='https://lol.com',
            message='Hello my name is Dmitro, i wanna enjoy in this city',
        )
        print(contact.is_report_sent)

        # Perform a POST request to trigger the view
        response = self.client.post('/give-contacts/')
        contact.is_report_sent = True
        contact.save()
        print(contact.is_report_sent)

        # Assert the expected behavior
        self.assertEqual(response.status_code, 200)

        # Get the updated contact object

        # Assert that the task has been triggered and the contact's is_report_sent flag is True
        self.assertTrue(contact.is_report_sent)
        self.assertTrue(send_contact_email.delay())

