from .models import Question, QuestionImage, Response
from django import forms


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': True,
                'placeholder': '質問タイトルを入力してください。'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '質問内容を入力してください。'
            }),
        }


QuestionImageFormSet = forms.inlineformset_factory(
    Question,
    QuestionImage,
    fields = '__all__',
    extra=1,
    max_num=3,
    can_delete=False,
)

class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': '回答内容を入力してください。'
            })
        }

class NewReplyForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '返信内容を入力してください。'
            })
        }
