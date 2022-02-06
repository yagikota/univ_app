# from django.contrib.auth import get_user_model
# from django.test import TestCase, RequestFactory
# from allauth.account.models import EmailAddress
# from main.models import Question, Likes
# from main.views import question_list, liked_question_list, my_question_list, delete_user_complete

# User = get_user_model()

# class LandPageTests(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='test1',
#             email='test1@edu.osakafu-u.ac.jp',
#             password='psst1'
#         )

#     def test_get_success_when_unauthenticated(self):
#         EmailAddress.objects.create(
#             user=self.user,
#             email="test1@edu.osakafu-u.ac.jp",
#             primary=True,
#             verified=False,
#         )
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)

#     def test_get_success_when_logged_in(self):
#         logged_in = self.client.login(username=self.user.username, password='psst1')
#         self.assertTrue(logged_in)
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)

#     def test_get_success_when_logged_out(self):
#         self.client.logout()
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)


# class LoginRequiredMixinTests(TestCase):

#     def setUp(self):
#         self.user1 = User.objects.create_user(
#             username='test1',
#             email='test1@edu.osakafu-u.ac.jp',
#             password='psst1'
#         )

#     def test_redirect_when_unauthenticated(self):
#         EmailAddress.objects.create(
#             user=self.user1,
#             email="test1@edu.osakafu-u.ac.jp",
#             primary=True,
#             verified=False,
#         )
#         response = self.client.get('/top_page/')
#         self.assertRedirects(response, '/accounts/login/?next=/top_page/')

#     def test_get_success_when_logged_in(self):
#         logged_in = self.client.login(username=self.user1.username, password='psst1')
#         self.assertTrue(logged_in)
#         response = self.client.get('/top_page/')
#         self.assertEqual(response.status_code, 200)

#     def test_redirect_when_logged_out(self):
#         logged_out = self.client.logout()
#         self.assertFalse(logged_out)
#         response = self.client.get('/top_page/')
#         self.assertRedirects(response, '/accounts/login/?next=/top_page/')


# class TopPageTests(LoginRequiredMixinTests):
#     def setUp(self):
#         super().setUp()
#         self.url_name = '/top_page/'


# def create_question(author, title, body):
#     return Question.objects.create(author=author, title=title, body=body)

# def create_likes(question, author):
#     return Likes.objects.create(question=question, author=author)


# class QuestionListViewTests(LoginRequiredMixinTests):

#     def setUp(self):
#         super().setUp()
#         self.user2 = User.objects.create_user(
#             username='test2',
#             email='test2@edu.osakafu-u.ac.jp',
#             password='psst2'
#         )
#         self.user3 = User.objects.create_user(
#             username='test3',
#             email='test3@edu.osakafu-u.ac.jp',
#             password='psst3'
#         )
#         self.question = create_question(author=self.user2, title='titlewewe', body="body")
#         create_likes(self.question, self.user3)
#         self.url_name = '/list/'
#         self.factory = RequestFactory()

#     def test_are_correct_context_data(self):
#         request = self.factory.get('/list/')
#         request.user = self.user3
#         response = question_list(request)
#         liked_list = response.context_data['liked_list']
#         self.assertIn(self.question.id, liked_list)

# class LikedQuestionListViewTests(LoginRequiredMixinTests):
#     def setUp(self):
#         super().setUp()
#         self.user2 = User.objects.create_user(
#             username='test2',
#             email='test2@edu.osakafu-u.ac.jp',
#             password='psst2'
#         )
#         self.user3 = User.objects.create_user(
#             username='test3',
#             email='test3@edu.osakafu-u.ac.jp',
#             password='psst3'
#         )
#         self.question = create_question(author=self.user2, title='titlewewe', body="body")
#         create_likes(self.question, self.user3)
#         self.url_name = '/like/'
#         self.factory = RequestFactory()

#     def test_are_correct_context_data(self):
#         request = self.factory.get('/like/')
#         request.user = self.user3
#         response = liked_question_list(request)
#         liked_list = response.context_data['liked_list']
#         self.assertIn(self.question.id, liked_list)

# class MyQuestionListViewTests(LoginRequiredMixinTests):
#     def setUp(self):
#         super().setUp()
#         self.user2 = User.objects.create_user(
#             username='test2',
#             email='test2@edu.osakafu-u.ac.jp',
#             password='psst2'
#         )
#         self.user3 = User.objects.create_user(
#             username='test3',
#             email='test3@edu.osakafu-u.ac.jp',
#             password='psst3'
#         )
#         self.question = create_question(author=self.user3, title='titlewewe', body="body")
#         create_likes(self.question, self.user3)
#         self.url_name = '/my_q_list/'
#         self.factory = RequestFactory()

#     def test_are_correct_context_data(self):
#         request = self.factory.get('/my_q_list/')
#         request.user = self.user3
#         response = my_question_list(request)
#         liked_list = response.context_data['liked_list']
#         self.assertIn(self.question.id, liked_list)

# class DeleteUserCompleteViewTests(LoginRequiredMixinTests):

#     def setUp(self):
#         super().setUp()
#         self.user2 = User.objects.create_user(
#             username='test2',
#             email='test2@edu.osakafu-u.ac.jp',
#             password='psst2'
#         )
#         self.factory = RequestFactory()


#     def test_successfully_deleted_user(self):
#         request = self.factory.get('/delete_complete/')
#         request.user = self.user2
#         response = delete_user_complete(request)
#         self.assertIsNone(User.objects.filter(email=request.user.email).first())





# """
# https://torajirousan.hatenadiary.jp/entry/2020/05/03/075635
# https://qiita.com/tmasuyama/items/efbbc0f3af52d6a5dee4#%E3%83%A6%E3%83%8B%E3%83%83%E3%83%88%E3%83%86%E3%82%B9%E3%83%88%E4%BD%9C%E6%88%90
# https://qiita.com/yukiya285/items/3b3265d745aef36f26ff
# https://qiita.com/okoppe8/items/eb7c3be5b9f6be244549
# https://qiita.com/tmasuyama/items/efbbc0f3af52d6a5dee4#test_modelspy
# https://qiita.com/0xfffffff7/items/b0c3a747522943df434f
# https://torajirousan.hatenadiary.jp/entry/2020/05/03/075635
# https://qiita.com/komedaoic/items/0057b55c8ba763bda6ca

# """
