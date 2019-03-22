from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.db.models import Avg
from .models import Genre, Movie, Score
from .forms import MovieForm, ScoreForm

# Create your views here.
def index(request):
    # movies = Movie.objects.annotate(score_avg=Avg('score__score')).all()
    movies = get_list_or_404(Movie.objects.annotate(score_avg=Avg('score__score')))
    context = {'movies':movies}
    return render(request, 'movies/index.html', context)

def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
    context = {'form': form}
    return render(request, 'movies/form.html', context)

def detail(request, movie_pk):
    # movie = Movie.objects.annotate(score_avg=Avg('score__score')).get(pk=movie_pk)
    movie = get_object_or_404(Movie.objects.annotate(score_avg=Avg('score__score')), pk=movie_pk)
    scores = movie.score_set.all()
    form = ScoreForm()
    context = {'movie': movie, 'scores': scores, 'form': form}

    '''
    # 방법 2
    movie = get_object_or_404(Movie, pk=movie_pk)
    score_avg = movie.score_set.aggregate(Avg('score')).get('score__avg') or 0.0
    scores = movie.score_set.all()
    form = ScoreForm()
    context = {'movie': movie, 'scores': scores, 'score_avg':score_avg, 'form': form}
    '''
    return render(request, 'movies/detail.html', context)

def update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {'form': form}
    return render(request, 'movies/form.html', context)

def delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies:index')
    else:
        return redirect('movies:detail', movie.pk)

def scores_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        '''
        방법 1. 
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = form.save(commit=False)
            score.movie = movie
            score.save()
        '''
        # 방법 2.
        score = Score(movie=movie)
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            score = form.save()
            return redirect('movies:detail', movie.pk)

    return redirect('movies:detail', movie.pk) 

def scores_delete(request, movie_pk, score_pk):
    score = get_object_or_404(Score, pk=score_pk)
    if request.method == 'POST':
    	score.delete()
    return redirect('movies:detail', movie_pk)
