from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage

from .forms import LoginForm, SignUpForm, SettingsForm, AskForm
from .models import Tag, Question, Answer, QuestionLike, AnswerLike

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
    form = AskForm()
    return render(request, 'main/ask.html', {
        'form': form,
    })


def question(request, pk=None):
    question = get_object_or_404(Question, id=pk)
    answers = question.answers.hot_answers()
    page, page_range = paginate(request, answers, 10, 5)
    return render(request, 'main/question.html', {
        'question': question,
        'answers': page.object_list,
        'page': page,
        'page_range': page_range,
    })

def login(request):
    form = LoginForm()
    return render(request, 'main/login.html', {
        'form': form,
    })

def signup(request):
    form = SignUpForm()
    return render(request, 'main/signup.html', {
        'form': form,
    })

def settings(request):
    form = SettingsForm()
    return render(request, 'main/settings.html', {
        'form': form,
    })


def tag(request, tag_name=None):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = tag.question_set.last_questions()
    page, page_range = paginate(request, questions, 10, 5)
    return render(request, 'main/tag.html', {
        'tag': tag,
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    })

def hot(request):
    questions = Question.objects.hot_questions()
    page, page_range = paginate(request, questions, 10, 5)
    return render(request, 'main/hot.html', {
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    })