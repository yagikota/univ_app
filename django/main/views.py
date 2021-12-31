from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView, TemplateView, View, CreateView
from .models import Question, Response, Likes
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewQuestionForm, NewReplyForm, NewResponseForm
from django.contrib.auth import get_user_model
from pure_pagination.mixins import PaginationMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from functools import reduce
from operator import and_

# Create your views here.
User = get_user_model()

class LandPage(TemplateView):
    template_name = 'main/landing_page.html'


land_page = LandPage.as_view()


class TopPage(LoginRequiredMixin, TemplateView):
    template_name = 'main/top_page.html'


top_page = TopPage.as_view()


class QuestionListView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'main/list.html'
    model = Question
    context_object_name = 'questions'
    paginate_by = 3

    # 検索の処理 改善の余地あり
    def search(self, model_obj, sort_order):
        sort_type = {
        'date_desc': '質問日時の新しい順',
        'date_asc': '質問日時の古い順',
        'ans_desc': '回答数の多い順',
        'ans_asc': '回答数の少ない順',
        'likes_desc': 'いいねの多い順',
        }
        keyword = self.request.GET.get('keyword')

        if keyword:
            keyword = keyword.replace(' ', '').replace('　', '')
            # print([Q(title__icontains=char) | Q(body__icontains=char) for char in keyword])
            query = reduce(and_, [Q(title__icontains=char) | Q(body__icontains=char) for char in keyword])
            # print(query)
            # print(type(query))
            model_obj = model_obj.filter(query)
            # print(model_obj)
            # model_obj = model_obj.filter(Q(title__icontains=char) | Q(body__icontains=char))
            messages.success(self.request, '「{0}」の検索結果 {1}'.format(keyword, sort_type[sort_order]))
        return model_obj

    def get_queryset(self):
        sort_order = self.request.GET.get('sort_order')
        if sort_order == 'date_desc':
            return self.search(Question.objects.order_by('-created_at'), sort_order)
        elif sort_order == 'date_asc':
            return self.search(Question.objects.order_by('created_at'), sort_order)
        elif sort_order == 'ans_desc':
            return self.search(Question.objects.annotate(num_responses=Count('responses')).order_by('-num_responses'), sort_order)
        elif sort_order == 'ans_asc':
            return self.search(Question.objects.annotate(num_responses=Count('responses')).order_by('num_responses'), sort_order)
        elif sort_order == 'likes_desc':
            return self.search(Question.objects.annotate(num_likes=Count('likes')).order_by('-num_likes'), sort_order)
        else:
            return self.search(Question.objects.order_by('-created_at'), sort_order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.all()
        liked_list = []
        for question in questions:
            liked = question.likes.filter(author=self.request.user)
            if liked.exists():
                liked_list.append(question.id)
        context['liked_list'] = liked_list
        return context


question_list = QuestionListView.as_view()


def likeview(request):
    if request.method =="POST":
        question = get_object_or_404(Question, pk=request.POST.get('question_id'))
        author = request.user
        liked = False
        like = Likes.objects.filter(question=question, author=author)
        if like.exists():
            like.delete()
        else:
            like.create(question=question, author=author)
            liked = True

        context={
            'question_id': question.id,
            'liked': liked,
            'count': question.likes.count(),
        }
        print(context)

    if request.is_ajax():
        return JsonResponse(context)

class LikedQuestionListView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'main/mypage/liked_question_list.html'
    context_object_name = 'liked_questions'
    paginate_by = 1

    # 自分がいいねした質問のquerysetを取得
    def get_queryset(self):
        id_list = [likes.question.id for likes in Likes.objects.filter(author=self.request.user)]
        question =  Question.objects.filter(id__in=id_list)
        sort_order = self.request.GET.get('sort_order')
        if sort_order == 'date_desc':
            return question.order_by('-created_at')
        elif sort_order == 'date_asc':
            return question.order_by('created_at')
        elif sort_order == 'ans_desc':
            return question.annotate(num_responses=Count('responses')).order_by('-num_responses')
        elif sort_order == 'ans_asc':
            return question.annotate(num_responses=Count('responses')).order_by('num_responses')
        else:
            return question.annotate(num_likes=Count('likes')).order_by('-num_likes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.all()
        liked_list = []
        for question in questions:
            liked = question.likes.filter(author=self.request.user)
            if liked.exists():
                liked_list.append(question.id)
        context['liked_list'] = liked_list
        return context


liked_question_list = LikedQuestionListView.as_view()


class MyQuestionListView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'main/mypage/my_question_list.html'
    context_object_name = 'my_questions'
    paginate_by = 1

    # 自分がした質問のquerysetを取得
    def get_queryset(self):
        question =  Question.objects.filter(author=self.request.user)
        sort_order = self.request.GET.get('sort_order')
        if sort_order == 'date_desc':
            return question.order_by('-created_at')
        elif sort_order == 'date_asc':
            return question.order_by('created_at')
        elif sort_order == 'ans_desc':
            return question.annotate(num_responses=Count('responses')).order_by('-num_responses')
        elif sort_order == 'ans_asc':
            return question.annotate(num_responses=Count('responses')).order_by('num_responses')
        else:
            return question.annotate(num_likes=Count('likes')).order_by('-num_likes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_questions = Question.objects.filter(author=self.request.user)
        liked_list = []
        for question in my_questions:
            liked = question.likes.filter(author=self.request.user)
            if liked.exists():
                liked_list.append(question.id)
        context['liked_list'] = liked_list
        return context


my_question_list = MyQuestionListView.as_view()


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'main/mypage/profile.html'


profile = ProfileView.as_view()

class DeleteUserComfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'main/mypage/delete_confirm.html'


delete_user_confirm = DeleteUserComfirmView.as_view()


class DeleteUserCompleteView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        # 大元のデータベースから削除
        User.objects.filter(email=self.request.user.email).delete()
        return render(self.request,'main/landing_page.html')


delete_user_complete = DeleteUserCompleteView.as_view()


# 質問する時の処理
class PostQuestionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'main/comment_create.html'
    # model = Question
    form_class = NewQuestionForm
    success_url = reverse_lazy('main:new_question')
    success_message = "質問を投稿しました。"

    def form_valid(self, form):
        # 重要
        # https://docs.djangoproject.com/ja/4.0/topics/class-based-views/generic-editing/#models-and-request-user
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        
        return form_class(**self.get_form_kwargs())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewQuestionForm()
        return context

post_question = PostQuestionView.as_view()

# def new_question_page(request):
#     form = NewQuestionForm()

#     if request.method == 'POST':
#         try:
#             form = NewQuestionForm(request.POST)
#             if form.is_valid():
#                 question = form.save(commit=False)
#                 question.author = request.user
#                 question.save()
#         except Exception as e:
#             messages.error(request, e)

#     context = {
#         'form': form,
#         'messages': messages,
#     }

#     return render(request, 'main/comment_create.html', context)

# 質問への返信の処理
def question_page(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                # commit=FalseとしてResponseのインスタンスを代入, commit=Trueだと
                response = response_form.save(commit=False)
                # formで入力されなかったfieldを入力
                response.author = request.user
                response.question = Question(id=id)
                response.save()
                return redirect('/question/'+str(id))
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(id=id)
    context = {
        'question': question,
        'response_form': response_form,
        'reply_form': reply_form,
    }
    return render(request, 'main/question.html', context)

# 返信に対する返信の処理
def replypage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.author = request.user
                reply.question = Question(id=question_id)
                reply.parent = Response(id=parent_id)
                reply.save()
                return redirect('/question/'+str(question_id))
        except Exception as e:
            print(e)
            raise

    return redirect('list')


class LoginAfterPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('password_change_done')


login_after_password_change = LoginAfterPasswordChangeView.as_view()


# pw変更後の遷移先
class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'account/password_change_done.html'


password_change_done = PasswordChangeDoneView.as_view()
