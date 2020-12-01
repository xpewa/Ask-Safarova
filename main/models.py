from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег',
        verbose_name_plural = 'Теги'

class QuestionManager(models.Manager):
    def last_questions(self):
        return self.order_by('-date_create')

    def hot_questions(self):
        return self.order_by('-rating')

class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    tags = models.ManyToManyField(Tag, null=True, blank=True, verbose_name='Теги')
    objects = QuestionManager()

    def update_rating(self):
        self.rating = 0
        for like in self.questionlike_set.all():
            self.rating += 1 if like.is_like else -1
        self.save()
        return self.rating

    def liked_users(self):
        return User.objects.filter(questionlike__question=self, questionlike__is_like=True)

    def disliked_users(self):
        return User.objects.filter(questionlike__question=self, questionlike__is_like=False)

    def __str__(self):
        return '{}; user: {}; date_create: {}'.format(self.title, self.user, self.date_create)

    class Meta:
        verbose_name = 'Вопрос',
        verbose_name_plural = 'Вопросы'

class AnswerManager(models.Manager):
    def hot_answers(self):
        return self.order_by('-rating', '-date_create')

class Answer(models.Model):
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name='Вопрос')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_correct = models.BooleanField(default=False)
    objects = AnswerManager()

    def update_rating(self):
        self.rating = 0
        for like in self.answerlike_set.all():
            self.rating += 1 if like.is_like else -1
        self.save()
        return self.rating

    def liked_users(self):
        return User.objects.filter(answerlike__answer=self, answerlike__is_like=True)

    def disliked_users(self):
        return User.objects.filter(answerlike__answer=self, answerlike__is_like=False)

    def corrected_answer(self):
        self.is_correct = True
        self.save()

    def __str__(self):
        return '{}; date_create: {}; {}'.format(self.user, self.date_create, self.text)

    class Meta:
        verbose_name = 'Ответ',
        verbose_name_plural = 'Ответы'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    nick_name = models.CharField(max_length=20, blank=True, verbose_name='Никнейм')
    avatar = models.ImageField(upload_to='avatars', default='avatars/default_avatar.jpg', verbose_name='Аватар')

    class Meta:
        verbose_name = 'Профиль',
        verbose_name_plural = 'Профили'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class QuestionLikeManager(models.Manager):
    def like(self, user, question, is_like):
        like, is_create = self.get_or_create(user=user, question=question)
        like.is_like = is_like
        like.save()
        return question.update_rating()

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    is_like = models.BooleanField(default=True)
    objects = QuestionLikeManager()

    class Meta:
        verbose_name = 'Лайк вопроса',
        verbose_name_plural = 'Лайки вопроса'

class AnswerLikeManager(models.Manager):
    def like(self, user, answer, is_like):
        like, is_create = self.get_or_create(user=user, answer=answer)
        like.is_like = is_like
        like.save()
        return answer.update_rating()

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
    is_like = models.BooleanField(default=True)
    objects = AnswerLikeManager()

    class Meta:
        verbose_name = 'Лайк ответа',
        verbose_name_plural = 'Лайки ответа'