from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('ask', views.ask),
    path('question', views.question),
    path('login', views.login),
    path('signup', views.signup),
    path('settings', views.settings),
    path('tag', views.tag),
    path('hot', views.hot),
]
