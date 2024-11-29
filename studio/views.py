from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import SignUpForm, RequestCreateForm, RequestDoneStatusChangeForm, RequestWorkStatusChangeForm, CategoryCreateForm

def index(request):
    done_requests = Request.objects.filter(status='В')[:4]
    accepted_request_counter = Request.objects.filter(status='П').count()
    return render(request, 'index.html', {
        'done_requests': done_requests, 'accepted_request_counter': accepted_request_counter}
    )


@login_required
def indexacc(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user_requests': user_requests})

@login_required
def indexacc_filter(request):
    user_filter_requests = Request.objects.filter(user=request.user, status=request.GET['status'][0])
    return render(request, 'profile.html', {'user_requests': user_filter_requests})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.fio = form.cleaned_data['fio']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def request_add(request):
    if request.method == 'POST':
        form = RequestCreateForm(request.POST, request.FILES)
        if form.is_valid():
            request_save = form.save(commit=False)
            request_save.user = request.user
            request_save.save()
            return redirect('profile')
    else:
        form = RequestCreateForm(initial={'user': request.user.pk})
    return render(request, 'request_add.html', {'form': form})

@login_required
def request_delete(request, pk):
    request_obj = Request.objects.get(id=pk)
    if request_obj.status == 'Н':
        return render(request, 'request_delete_confirm.html', {'request': request_obj})

@login_required
def request_delete_confirm(request, pk):
    request = Request.objects.get(id=pk)
    request.delete()
    return redirect('profile')

@login_required
def requests(request):
    new_requests = Request.objects.filter(status='Н')
    context = {'new_requests': new_requests}
    return render(request, 'requests.html', context)

@login_required
def request_done_change(request, pk):
    request_instance = Request.objects.get(id=pk)
    if request.method == 'POST':
        form = RequestDoneStatusChangeForm(request.POST, request.FILES, instance=request_instance)
        if form.is_valid():
            request = form.save(commit=False)
            request.status = 'В'
            request.save()
            return redirect('requests')
    else:
        form = RequestDoneStatusChangeForm(initial={'status': 'D'})
    return render(request, 'request_done_change.html', {'form': form})

@login_required
def request_work_change(request, pk):
    request_instance = Request.objects.get(id=pk)
    if request.method == 'POST':
        form = RequestWorkStatusChangeForm(request.POST, request.FILES, instance=request_instance)
        if form.is_valid():
            request = form.save(commit=False)
            request.status = 'П'
            request.save()
            return redirect('requests')
    else:
        form = RequestWorkStatusChangeForm(initial={'status': 'A'})
    return render(request, 'request_work_change.html', {'form': form})

@login_required
def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'categories.html', context)

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('categories')
    else:
        form = CategoryCreateForm()
    return render(request, 'category_create.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('categories')

from captcha.image import ImageCaptcha
from PIL import Image, ImageDraw, ImageFont
import random
from django.http import JsonResponse

class CustomCaptcha(ImageCaptcha):
    def generate_captcha(self, width, height, length):
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        captcha_text = ''.join(random.choices('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', k=length))
        font = ImageFont.truetype('arial.ttf', 36)
        text_width, text_height = draw.textsize(captcha_text, font=font)
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        draw.text((x, y), captcha_text, font=font, fill=(0, 0, 0))
        for _ in range(100):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            draw.point((x, y), fill=(0, 0, 0))
        return image, captcha_text
