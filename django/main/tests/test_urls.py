from django.test import TestCase
from django.urls import reverse, resolve
from main import views 

class UrlsTests(TestCase):

    def setUp(self):
        self.app_name = 'main'

    def reverse_url(self, name):
        url_pattern_name = self.app_name + ':' + name
        return reverse(url_pattern_name)

    def test_land_page_url_is_resolved(self):
        url = self.reverse_url('land_page')
        self.assertEqual(resolve(url).func, views.land_page)

    def test_top_page_url_is_resolved(self):
        url = self.reverse_url('top_page')
        self.assertEqual(resolve(url).func, views.top_page)

    def test_list_url_is_resolved(self):
        url = self.reverse_url('list')
        self.assertEqual(resolve(url).func, views.question_list)

    def test_liked_list_url_is_resolved(self):
        url = self.reverse_url('liked_list')
        self.assertEqual(resolve(url).func, views.liked_question_list)

    def test_my_q_list_url_is_resolved(self):
        url = self.reverse_url('my_q_list')
        self.assertEqual(resolve(url).func, views.my_question_list)

    def test_like_url_is_resolved(self):
        url = self.reverse_url('like')
        self.assertEqual(resolve(url).func, views.likeview)

    def test_profile_url_is_resolved(self):
        url = self.reverse_url('profile')
        self.assertEqual(resolve(url).func, views.profile)

    def test_delete_confirm_url_is_resolved(self):
        url = self.reverse_url('delete_confirm')
        self.assertEqual(resolve(url).func, views.delete_user_confirm)

    def test_new_question_url_is_resolved(self):
        url = self.reverse_url('new_question')
        self.assertEqual(resolve(url).func, views.new_question_page)

    def test_question_url_is_resolved(self):
        url = reverse('main:question', args=[1])
        self.assertEqual(resolve(url).func, views.question_page)

    def test_reply_url_is_resolved(self):
        url = self.reverse_url('reply')
        self.assertEqual(resolve(url).func, views.replypage)
