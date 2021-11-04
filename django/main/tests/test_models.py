from django.contrib.auth import get_user_model
from django.test import TestCase
from main.models import Question, Response, Likes

User = get_user_model()

def create_user(username, email, password):
    return User.objects.create_user(username=username, email=email, password=password)

def create_question(author, title, body):
    return Question.objects.create(author=author, title=title, body=body)

def create_response(author, question, body, parent=None):# parent=Noneの場合、質問に対する返信
    return Response.objects.create(author=author, question=question, body=body, parent=parent)

def create_likes(question, author):
    return Likes.objects.create(question=question, author=author)

class UserModelTests(TestCase):
    
    def test_is_empty(self):
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 0)

    def test_is_count_one(self):
        create_user('test1', 'test1@edu.osakafu-u.ac.jp', 'psst1')
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 1)

    def assertEqualUserModel(self, actual_user, username, email, password):
        self.assertEqual(actual_user.username, username)
        self.assertEqual(actual_user.email, email)
        self.assertTrue(actual_user.check_password(password))

    def test_saving_and_retrieving_user(self):
        username, email, password = 'test1', 'test1@edu.osakafu-u.ac.jp', 'psst1'
        create_user(username, email, password)
        saved_users = User.objects.all()
        actual_user = saved_users[0]
        self.assertEqualUserModel(actual_user, username, email, password)



class QuestionTests(TestCase):

    def setUp(self):
        self.user1 = create_user('test1', 'test1@edu.osakafu-u.ac.jp', 'psst1')
        self.user2 = create_user('test2', 'test2@edu.osakafu-u.ac.jp', 'psst2')
        self.user3 = create_user('test3', 'test3@edu.osakafu-u.ac.jp', 'psst3')

    def test_is_empty(self):
        saved_questions = Question.objects.all()
        self.assertEqual(saved_questions.count(), 0)

    def test_is_count_one(self):
        create_question(self.user1, 'test title1', 'test body test body test body test body test body test body')
        saved_questions = Question.objects.all()
        self.assertEqual(saved_questions.count(), 1)

    def assertEqualQuestionModel(self, actual_question, author, title, body):
        self.assertEqual(actual_question.author, author)
        self.assertEqual(actual_question.title, title)
        self.assertEqual(actual_question.body, body)

    def test_saving_and_retrieving_question(self):
        author = self.user2
        title = 'test title2'
        body = 'test body test body test body test body test body test body'
        create_question(author, title, body)
        saved_questions = Question.objects.all()
        actual_question = saved_questions[0]
        self.assertEqualQuestionModel(actual_question, author, title, body)

    def test_get_responses(self):
        question = create_question(self.user3, 'test title3', 'test body test body test body test body test body test body')
        response = create_response(self.user2, question, 'response response response response response response response')
        self.assertEqual(question.get_responses()[0], response)


class ResponseTests(TestCase):

    def setUp(self):
        self.user1 = create_user('test1', 'test1@edu.osakafu-u.ac.jp', 'psst1')
        self.user2 = create_user('test2', 'test2@edu.osakafu-u.ac.jp', 'psst2')
        self.user3 = create_user('test3', 'test3@edu.osakafu-u.ac.jp', 'psst3')
        self.question = create_question(self.user1, 'test title1', 'test body test body test body test body test body test body')

    def test_is_empty(self):
        saved_responses = Response.objects.all()
        self.assertEqual(saved_responses.count(), 0)

    def test_is_count_one(self):
        create_response(self.user1, self.question, 'response response response response response response response')
        saved_responses = Response.objects.all()
        self.assertEqual(saved_responses.count(), 1)

    def assertEqualResponseModel(self, actual_response, author, question, body):
        self.assertEqual(actual_response.author, author)
        self.assertEqual(actual_response.question, question)
        self.assertEqual(actual_response.body, body)

    def test_saving_and_retrieving_response(self):
        author = self.user2
        question=self.question
        body='response response response response response response response'
        create_response(author, question, body)
        saved_responses = Response.objects.all()
        actual_response = saved_responses[0]
        self.assertEqualResponseModel(actual_response, author, question, body)

    def test_get_responses(self):
        question = create_question(self.user3, 'test title3', 'test body test body test body test body test body test body')
        response1 = create_response(self.user2, question, 'response response response response response response response')
        response2 = create_response(self.user3, question, 'response response response response response response response', response1)
        self.assertEqual(response1.get_responses()[0], response2)

class LikesTests(TestCase):

    def setUp(self):
        self.user1 = create_user('test1', 'test1@edu.osakafu-u.ac.jp', 'psst1')
        self.user2 = create_user('test2', 'test2@edu.osakafu-u.ac.jp', 'psst2')
        self.question = create_question(self.user1, 'test title1', 'test body test body test body test body test body test body')

    def test_is_empty(self):
        saves_likes = Likes.objects.all()
        self.assertEqual(saves_likes.count(), 0)

    def test_is_count_one(self):
        create_likes(self.question, self.user2)
        saves_likes = Likes.objects.all()
        self.assertEqual(saves_likes.count(), 1)

    def assertEqualLikesModel(self, actual_likes, question, author):
        self.assertEqual(actual_likes.question, question)
        self.assertEqual(actual_likes.author, author)

    def test_saving_and_retrieving(self):
        question, author = self.question, self.user2
        create_likes(question, author)
        saved_likes = Likes.objects.all()
        actual_likes = saved_likes[0]
        self.assertEqualLikesModel(actual_likes, question, author)















'''
ユーザー1がサイトのトップページに訪問 ok
会員登録ボタン押す
    (会員登録していない場合)
    会員登録formに遷移
    メールアドレス(必須)、ユーザー名(3文字以上, 必須)、パスワード(必須)入力
    (正しく入力された場合)
        メール受信
        メールのurlクリック(期限)
        メールアドレスの確認画面に遷移
        確認ボタン押す(期限ない?,  押さないと確認済みにならない, 押すと確認済みになり、ログインできる)
        ログインformに遷移
        ログインボタン押す
        トップページに遷移
    (正しく入力されなかった場合)
        ユーザー登録できない
    (会員登録していて,ログインしている場合)
    トップページに遷移
    (会員登録していて、ログインしていない場合)
    会員登録formに遷移
ログインボタン押す
    (会員登録していない場合)
    ログインformに遷移
    (会員登録していて,ログインしている場合)
    トップページに遷移
    (会員登録していて、ログインしていない場合)
    ログインformに遷移
    ユーザー名(必須)、パスワード(必須)入力
    (正しく入力された場合)
        トップページに遷移
    (正しく入力されなかった場合)
        トップページに遷移できない
'''