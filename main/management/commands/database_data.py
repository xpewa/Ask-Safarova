import random

from django.core.management.base import BaseCommand

from main.models import User, Tag, Question, Answer, QuestionLike, AnswerLike

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Создание пользователей
        for i in range(0, 10001):
            user = User.objects.create_user("username_" + str(i),
                password = "123456",
                email = "email_" + str(i)
            )
            user.profile.nick_name = "nick_name_" + str(i)
            user.save()
        users = User.objects.all()

        # Создание тегов
        for i in range(0, 10001):
            try:
                Tag(name="тег_"+str(i)).save()
            except Exception:
                pass
        tags = Tag.objects.all()

        # Создание вопросов
        for i in range(0, 100001):
            q = Question(
                title="Заголовок вопроса " + str(i),
                text=("Текст вопроса " + str(i) + " ") * random.randint(1, 50),
                user=random.choice(users),
            )
            q.save()
            for _ in range(0, random.randint(0, 3)):
                q.tags.add(random.choice(tags))
        questions = Question.objects.all()

        # Создание ответов
        for i in range(0, 1000001):
            Answer(
                text=("Текст ответа " + str(i) + " ") * random.randint(1, 50),
                is_correct=bool(random.randint(0, 1)),
                question=random.choice(questions),
                user=random.choice(users)
            ).save()
        answers = Answer.objects.all()

        # Создание лайков вопросов
        for _ in range(0, 1000001):
            like = QuestionLike(
                question=random.choice(questions),
                user=random.choice(users),
                is_like=bool(random.randint(0, 1))
            )
            like.save()
            if like.is_like:
                like.question.rating += 1
            else:
                like.question.rating -= 1
            like.question.save()

        # Создание лайков ответов
        for _ in range(0, 1000001):
            like = AnswerLike(
                answer=random.choice(answers),
                user=random.choice(users),
                is_like=bool(random.randint(0, 1))
            )
            like.save()
            if like.is_like:
                like.answer.rating += 1
            else:
                like.answer.rating -= 1
            like.answer.save()
# python manage.py database_data