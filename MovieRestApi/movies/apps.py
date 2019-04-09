from django.apps import AppConfig
from django.db.models.signals import pre_save


class MoviesConfig(AppConfig):
    name = 'movies'

    # def ready(self):
    #     from MovieRestApi import .tests

    # def ready(self):
    #     # importing model classes
    #     from .models import Movie
    #     Movie = self.get_model('Movie')
    #
    #     # registering signals with the model's string label
    #     pre_save.connect(receiver, sender='movie.Movie')