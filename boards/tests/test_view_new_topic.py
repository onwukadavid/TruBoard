from django.urls import reverse, resolve
from django.test import TestCase

from ..views import  new_topic
from ..models import Board,Topic,User
from ..forms import NewTopicForm


class NewTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Boards')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.login(username='john', password='123')


    def test_new_topic_view_status_code(self):
        url=reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)


    def test_new_topic_view_contains_link_back_to_boards_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk':1})
        board_topics_url = reverse('board_topics', kwargs={'pk':1})
        response=self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))
        

    def test_crsf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')


    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum sit dolor amet'
        }
        self.client.post(url,data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Topic.objects.exists())


    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic',kwargs={'pk':1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)


    def test_new_topic_invalid_post_data_empty_field(self):
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject':'',
            'message':''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Topic.objects.exists())


    def test_contains_forms(self):
        url = reverse('new_topic',kwargs={'pk':1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        user = Board.objects.create(name='Django', description='Django boards')
        self.url = reverse('new_topic', kwargs={'pk':1})
        self.response = self.client.get(self.url)


    def test_redirect(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))