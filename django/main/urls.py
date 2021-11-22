from django.urls import path
from main import views

app_name  = 'main'

urlpatterns = [
    path('', views.land_page, name='land_page'),
    path('top_page/', views.top_page, name='top_page'),
    path('list/', views.question_list, name='list'),
    path('liked_list/', views.liked_question_list,name='liked_list'),
    path('my_q_list', views.my_question_list, name='my_q_list'),
    path('like/', views.likeview, name='like'),
    path('profile/', views.profile, name='profile'),
    path('delete_confirm/', views.delete_user_confirm, name='delete_confirm'),
    path('delete_complete/', views.delete_user_complete, name='delete_complete'),
    path('new_question/', views.post_question, name='new_question'),
    path('question/<int:id>/', views.question_page, name='question'),
    path('reply/', views.replypage, name='reply'), 
]
