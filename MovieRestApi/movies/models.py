from django.db import models


class Movie(models.Model):
    movie_title = models.CharField(unique=True, max_length=100)
    omdb_details = models.TextField()
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.movie_title


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    comment_txt = models.TextField()
    date = models.DateField(auto_now=True, blank=False)

    def __str__(self):
        return str(self.movie_id)
