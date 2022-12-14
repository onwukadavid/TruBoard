from django.contrib.auth.models import User
from django.test import TestCase
from ..views import PostListView
from ..models import Board, Topic, Post
from django.urls import resolve, reverse


class TopicPostsTest(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='Django boards')
        user = User.objects.create_user(username='truman', email='truman@david.com', password='123')
        topic = Topic.objects.create(subject='Hello World', board=board, starter=user)
        Post.objects.create(message='lorem ipsum sit dolor amet', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk':board.pk,'topic_pk':topic.pk})
        self.response = self.client.get(url)


    def test_topic_posts_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_topic_posts_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)
