from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('question/<int:pk>', views.question, name='question'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('settings', views.settings, name='settings'),
    path('tag/<int:pk>', views.tag, name='tag'),
    path('hot', views.hot, name='hot'),
]
