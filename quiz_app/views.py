from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from .models import Question, UserProfile
from .forms import ProfileForm
import random

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('quiz:login')

class CustomLoginView(LoginView):
    template_name = 'quiz_app/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'title': 'Login to Quiz App'
    }

    def get(self, request, *args, **kwargs):
        if request.GET.get('registered') == 'true':
            messages.success(request, 'Registration successful! Please login.')
        return super().get(request, *args, **kwargs)

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'quiz_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = request.POST.get('email', '')
                user.save()
                return redirect(reverse('quiz:login') + '?registered=true')
            except Exception as e:
                form.add_error(None, f"Registration error: {str(e)}")
        return render(request, 'quiz_app/register.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.userprofile
    return render(request, 'quiz_app/profile.html', {'profile': profile})

class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'quiz_app/profile_edit.html'
    success_url = reverse_lazy('quiz:profile')

    def get_object(self):
        return self.request.user.userprofile

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        if 'asked_questions' in request.session:
            del request.session['asked_questions']
        return render(request, 'quiz_app/home.html')

class QuizView(View):
    def get(self, request):
        if 'asked_questions' not in request.session:
            request.session['asked_questions'] = []
            
        available_questions = Question.objects.exclude(
            id__in=request.session['asked_questions']
        )
        
        if available_questions.exists():
            question = random.choice(available_questions)
            request.session['asked_questions'].append(question.id)
            request.session.modified = True
            choices = list(question.choices.all())
            random.shuffle(choices)
            return render(request, 'quiz_app/quiz.html', {
                'question': question,
                'choices': choices,
                'time_limit': 30
            })
        return redirect('quiz:home')

class CheckAnswerView(View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        selected_choice = request.POST.get('choice')
        correct_choice = question.choices.filter(is_correct=True).first()
        
        is_correct = False
        if selected_choice and correct_choice:
            is_correct = int(selected_choice) == correct_choice.id
            
        result = {
            'question_text': question.question_text,
            'is_correct': is_correct,
            'correct_answer': correct_choice.choice_text,
            'explanation': question.explanation
        }
        
        if 'quiz_results' not in request.session:
            request.session['quiz_results'] = []
        request.session['quiz_results'].append(result)
        request.session.modified = True
        
        return render(request, 'quiz_app/result.html', {
            'question': question,
            'is_correct': is_correct,
            'correct_answer': correct_choice,
            'selected_choice_id': selected_choice
        })

class ResultsView(View):
    def get(self, request):
        results = request.session.get('quiz_results', [])
        total = len(results)
        correct = sum(1 for r in results if r['is_correct'])
        score_percent = int((correct/total)*100) if total > 0 else 0
        
        return render(request, 'quiz_app/results.html', {
            'results': results,
            'total': total,
            'correct': correct,
            'score_percent': score_percent
        })
