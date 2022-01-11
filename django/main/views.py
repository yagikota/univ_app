from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View, CreateView
from .models import Question, Response, Likes
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewQuestionForm, NewReplyForm, NewResponseForm, QuestionImageFormSet
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
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from config.settings.base import DEFAULT_FROM_EMAIL

# Create your views here.
User = get_user_model()

class LandPage(TemplateView):
    template_name = 'main/landing_page.html'


land_page = LandPage.as_view()


class TopPage(LoginRequiredMixin, TemplateView):
    template_name = 'main/top_page.html'


top_page = TopPage.as_view()


class QuestionListView(PaginationMixin, ListView):
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

        # responseとして渡される
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
        # 改善の余地あり
        elif sort_order == 'ans_desc':
            return question.annotate(num_responses=Count('responses')).order_by('-num_responses')
        # 改善の余地あり
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
    form_class = NewQuestionForm
    success_url = reverse_lazy('main:list')

    def get_context_data(self, **kwargs):
        context = super(PostQuestionView, self).get_context_data(**kwargs) # ?
        # context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['question_images'] = QuestionImageFormSet(self.request.POST)
        else:
            context['question_images'] = QuestionImageFormSet()
        return context

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     files = request.FILES.getlist('file_field')
    #     print(files)
    #     if form.is_valid():
    #         for file in files:
    #             print(file)
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        question_images = context['question_images']
        form.instance.author = self.request.user
        if question_images.is_valid():
            self.object = form.save()
            question_images.instance = self.object
            question_images.save()

        messages.success(self.request, '質問を投稿しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form)
        messages.error(self.request, '質問の投稿に失敗しました。')
        return super().form_invalid(form)

post_question = PostQuestionView.as_view()

# 質問への返信の処理
class QuestionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'main/question.html'
    # response_form
    form_class = NewResponseForm

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        question = Question.objects.get(id=self.kwargs['id'])
        reply_form = NewReplyForm()
        context['question'] = question
        context['reply_form'] = reply_form
        print(question.image)
        return context

    # 回答がついたことを通知
    def notify(self, form):
        context = {
            'user': self.request.user,
            'scheme': self.request.scheme,
            'domain': self.request.get_host(),
            'id': self.kwargs['id'],
            'body': form.cleaned_data['body'][:10],
        }
        subject = render_to_string('mail/get_answer/subject.txt', context, self.request)
        message = render_to_string('mail/get_answer/message.txt', context, self.request)
        from_email = DEFAULT_FROM_EMAIL
        to_email = self.request.user.email
        email = EmailMessage(
            subject,
            message,
            from_email,
            [to_email],
        )
        email.send()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question = Question(id=self.kwargs['id'])
        self.notify(form)
        messages.success(self.request, '回答を投稿しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '回答の投稿に失敗しました。')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('main:question', kwargs={'id': self.kwargs['id']})


question = QuestionView.as_view()

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
