from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from .forms import UserRegister
from django.db import models
from .models import *
from django.core.paginator import Paginator

# Create your views here.

def menu(request):
    title = 'Главная страница'
    context = {
        'title': title,
    }
    return render(request, 'platform.html', context)


def games(request):
    title ='Игры'
    # all_games = ['Atomic Heart', 'Cyberpunk 2077', 'PayDay 2']
    all_games = Game.objects.all()
    buy = 'Купить'
    context = {
        'title': title,
        'all_games': all_games,
        'buy': buy
    }
    return render(request, 'games.html', context)


def cart(request):
    title = 'Корзина'
    text = 'Извините, Ваша корзина пуста'
    context = {
        'title': title,
        'text': text,
    }
    return render(request, 'cart.html', context)


def sign_up_by_html(request):
    # users = ['Ivan', 'Petr', 'Tina']
    users = Buyer.objects.values_list('name', flat=True)
    info = {}
    if request.method == 'POST':
        user_exists = False
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age'))
        is_user = username in users
        if is_user:
            info['error'] = 'Пользователь уже существует'
            print(info['error'])
            return HttpResponse(info['error'])
        passwords_matched = password == repeat_password
        if passwords_matched:
            if age >= 18:
                user_exists = True
            else:
                info['error'] = 'Вы должны быть старше 18'
        else:
            info['error'] = 'Пароли не совпадают'

        if user_exists:
            new_user = Buyer.objects.create(name=username, balance=10000, age=age)
            message = f'Приветствуем, {new_user.name}!'
        else:
            message = info['error']
        print(message)

        return HttpResponse(message)
    return render(request, 'registration_page.html', info)


# создаем forms.py  в приложении task5
def sign_up_by_django(request):
    # users = ['Ivan', 'Petr', 'Tina']
    users = Buyer.objects.values_list('name', flat=True)
    info = {}
    message = ''
    if request.method == 'POST':
        user_exists = False
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = int(form.cleaned_data['age'])
            is_user = username in users
            if is_user:
                info['error'] = 'Пользователь уже существует'
                print(info['error'])
                return HttpResponse(info['error'])
            passwords_matched = password == repeat_password
            if passwords_matched:
                if age >= 18:
                    user_exists = True
                else:
                    info['error'] = 'Вы должны быть старше 18'
            else:
                info['error'] = 'Пароли не совпадают'

            if user_exists:
                new_user = Buyer.objects.create(name=username, balance=10000, age=age)
                message = f'Приветствуем, {new_user.name}!'
            else:
                message = info['error']
            print(message)
        return HttpResponse(message)
    else:
        form = UserRegister()
    info['form'] = form
    return render(request, 'registration_page.html', info)


def news(request):
    # Получаем все новости из базы данных
    news_list = News.objects.all().order_by('-date')  # Сортировка по дате (новые сначала)
    paginator = Paginator(news_list, 5) # Создаем Paginator, разбивая новости на страницы по 5 записей на страницу
    page_number = request.GET.get('page') # Получаем номер текущей страницы из GET-параметра
    page_obj = paginator.get_page(page_number) # Получаем объект страницы
    context = {
        'page_obj': page_obj,
    } # Передаем объект страницы в контекст

    return render(request, 'news.html', context)


