from django.db import models


# Create your models here.
class Movie(models.Model):
    movie_title = models.CharField(max_length=100)

    def __str__(self):
        return self.movie_title


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment_txt = models.TextField()
    date = models.DateField(auto_now=True, blank=False)

    def __str__(self):
        return self.movie_id
