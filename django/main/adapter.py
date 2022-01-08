from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


# OMUに対応させる
class ExtendedAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if "@edu.osakafu-u.ac.jp" not in email:
            raise forms.ValidationError("登録に使えるのは@edu.osakafu-u.ac.jpを持つメールアドレスのみです。")
        User.objects.filter(email=email, is_active=False).delete()
        return email
