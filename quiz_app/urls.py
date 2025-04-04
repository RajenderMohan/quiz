from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (HomeView, QuizView, CheckAnswerView, 
                   ResultsView, RegisterView, profile_view,
                   ProfileUpdateView)

app_name = 'quiz'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('', auth_views.LoginView.as_view(template_name='quiz_app/index.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('quiz/', QuizView.as_view(), name='start_quiz'),
    path('quiz/<int:question_id>/check/', CheckAnswerView.as_view(), name='check_answer'),
    path('results/', ResultsView.as_view(), name='results'),
]
