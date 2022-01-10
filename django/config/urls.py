from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import login_after_password_change, PasswordChangeDoneView

urlpatterns = [
                path('admin/', admin.site.urls),
                path('', include('main.urls')),
                path('accounts/password/change/', login_after_password_change, name='account_change_password'), # before allauth urls to override
                path('accounts/password/change/done', PasswordChangeDoneView.as_view(),name='password_change_done'),
                path('accounts/', include('allauth.urls')),
            ] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
