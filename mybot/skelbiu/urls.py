from django.urls import path

from . import views

app_name = 'skelbiu'
urlpatterns = [
    path('run_bot/', views.run_bot, name='run_bot'),
]
