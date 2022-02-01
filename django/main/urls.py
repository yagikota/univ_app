from django.urls import path
from main import views
app_name  = 'main'

urlpatterns = [
    path('', views.land_page, name='land_page'),
    path('list/', views.question_list, name='list'),
    path('liked_list/', views.liked_question_list,name='liked_list'),
    path('my_q_list', views.my_question_list, name='my_q_list'),
    path('like/', views.likeview, name='like'),
    path('profile/', views.profile, name='profile'),
    path('delete_confirm/', views.delete_user_confirm, name='delete_confirm'),
    path('delete_complete/', views.delete_user_complete, name='delete_complete'),
    path('post_question/', views.post_question, name='post_question'),
    path('question/<int:id>/', views.question, name='question'),
    path('question/<int:id>/solved_or_not/', views.solved_or_not_view, name='solved_or_not'),
    path('reply/', views.replypage, name='reply'), 
    path('question/<int:id>/edit/', views.edit, name='edit')
]
