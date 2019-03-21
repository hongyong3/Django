from django.shortcuts import render, redirect
from django.db.models import Avg
from .models import Movie, Genre, Score

# Create your views here.
def index(request):
    # movies = Movie.objects.order_by('-pk')
    movies = Movie.objects.annotate(score_avg=Avg('score__score')).all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    # movie = Movie.objects.get(pk=movie_pk)
    movie = Movie.objects.annotate(score_avg=Avg('score__score')).get(pk=movie_pk)
    scores = movie.score_set.all()
    genre = Genre.objects.get(pk=movie.genre_id)
    context = {
        'movie': movie,
        'genre': genre,
        'scores': scores,
    }
    return render(request, 'movies/detail.html', context)

def delete(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies:index')
    else:
        return redirect('movies:detail', movie_pk)

# 추가 사항(영화 정보 수정)
def edit(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.audience = request.POST.get('audience')
        movie.poster_url = request.POST.get('poster_url')
        movie.description = request.POST.get('description')
        movie.genre_id = request.POST.get('genre')
        movie.save()
        return redirect('movies:detail', movie_pk)
    else:
        genres = Genre.objects.all()
        context = {
            'movie': movie,
            'genres': genres,
        }
        return render(request, 'movies/edit.html', context)

def scores_create(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.method == 'POST':
        score = request.POST.get('score')
        content = request.POST.get('content')
        score = Score(movie=movie, score=score, content=content)
        score.save()
    return redirect('movies:detail', movie_pk)


def scores_delete(request, movie_pk, score_pk):
    score = Score.objects.get(pk=score_pk)
    if request.method == 'POST':
        score.delete()
    return redirect('movies:detail', movie_pk)
