from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('<int:movie_pk>/scores/<int:score_pk>/delete/', views.scores_delete, name='scores_delete'),
    path('<int:movie_pk>/scores/new/', views.scores_create, name='scores_create'),
    path('<int:movie_pk>/delete/', views.delete, name='delete'),
    path('<int:movie_pk>/edit/', views.update, name='update'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('new/', views.create, name='create'),
    path('', views.index, name='index'),
]
