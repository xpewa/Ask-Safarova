from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.contrib import auth
from django.http import HttpResponseRedirect

from .forms import LoginForm, SignUpForm, SettingsForm, AskForm, AnswerForm
from .models import Tag, Question, Answer, QuestionLike, AnswerLike

import re
import math

#Функция пагинации
def paginate(request, objects_list, default_limit=10, pages_count=None):
    try:
        limit = int(request.GET.get('limit', default_limit))
    except ValueError:
        limit = default_limit
    if limit > 100:
        limit = default_limit
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise 404

    paginator = Paginator(objects_list, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    if not pages_count:
        page_range = paginator.page_range
    else:
        start = page.number - pages_count
        if start < 0:
            start = 0
        page_range = paginator.page_range[start: page.number + int(pages_count / 2)]
    return page, page_range

def get_continue(request, default='/'):
    url = request.GET.get('next', default)
    if re.match(r'^/|http://127\.0\.0\.', url):   # Защита от Open Redirect
        return url
    return default

def index(request):
    questions = Question.objects.last_questions()
    page, page_range = paginate(request, questions, 10, 5)

    context = {
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    }
    return render(request, 'main/index.html', context)

def ask(request):
    if request.method == "POST":
        form = AskForm(request.user, request.POST)
        if form.is_valid():
            q = form.save()
            return HttpResponseRedirect('/question/' + str(q.pk))
    else:
        form = AskForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'main/ask.html', context)


def question(request, pk=None):
    q = get_object_or_404(Question, id=pk)

    if request.method == "POST":
        form = AnswerForm(request.user, q, request.POST)
        if form.is_valid():
            new_answer = form.save()
            answers = q.answers.hot_answers()
            #Индекс нового ответа
            index_answer = 1
            for ans in answers:
                if ans == new_answer:
                    break
                index_answer += 1
            page = math.ceil(index_answer / 10)
            return HttpResponseRedirect('/question/{}?page={}#answer_{}'.format(pk, page, new_answer.pk))
    else:
        form = AnswerForm(request.user, q)

    answers = q.answers.hot_answers()
    page, page_range = paginate(request, answers, 10, 5)
    context = {
        'question': q,
        'answers': page.object_list,
        'page': page,
        'page_range': page_range,
        'form': form,
    }
    return render(request, 'main/question.html', context)

def login(request):
    url = get_continue(request)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.auth())
            return HttpResponseRedirect(url)
    else:
        form = LoginForm()
    context = {
        'form': form,
        'next_url': url,
    }
    return render(request, 'main/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(get_continue(request))

def signup(request):
    url = get_continue(request)
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login?next=' + url)
    else:
        form = SignUpForm()
    context = {
        'form': form,
        'next_url': url,
    }
    return render(request, 'main/signup.html', context)

def settings(request):
    user = request.user
    if request.method == "POST":
        form = SettingsForm(user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/settings')
    else:
        form = SettingsForm(user, initial={'username' : user.username,
                                            'email': user.email,
                                            'nick_name': user.profile.nick_name,
                                            'avatar': user.profile.avatar})
    context = {
        'form': form,
    }
    return render(request, 'main/settings.html', context)


def tag(request, tag_name=None):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = tag.question_set.last_questions()
    page, page_range = paginate(request, questions, 10, 5)
    context = {
        'tag': tag,
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    }
    return render(request, 'main/tag.html', context)

def hot(request):
    questions = Question.objects.hot_questions()
    page, page_range = paginate(request, questions, 10, 5)
    context = {
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    }
    return render(request, 'main/hot.html', context)