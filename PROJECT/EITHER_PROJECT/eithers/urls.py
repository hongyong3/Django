from django.urls import path
from . import views

app_name = 'eithers'

urlpatterns = [
    path('random/', views.random, name='random'),
    path('<int:question_pk>/comments/<int:answer_pk>/delete/', views.answers_delete, name='answers_delete'),
    path('<int:question_pk>/comments/', views.answers_create, name='answers_create'),
    path('<int:question_pk>/', views.detail, name='detail'),
    path('new/', views.new, name='new'), # GET(new), POST(create)
    path('', views.index, name='index'),
]
