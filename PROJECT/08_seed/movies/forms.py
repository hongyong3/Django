from django import forms
from .models import Movie, Score

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['content', 'score',]
        widgets = {
           'score': forms.NumberInput(attrs={'min': '0', 'max': '5', })}

