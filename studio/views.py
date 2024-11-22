from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    return render(
        request,
        'index.html',
    )
# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/studio')  # Замените 'home' на ваше целевое представление
    else:
        form = AuthenticationForm()
    return render(request, '/login.html', {'form': form})

class MyProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'protected_page.html'