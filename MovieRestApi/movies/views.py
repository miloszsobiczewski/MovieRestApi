from django.shortcuts import render
from rest_framework import viewsets
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import pdb
from django.db.models import Avg, Count, Min, Sum

class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(methods=['GET'], detail=False)
    def top(self, request):
        # pdb.set_trace()
        date_from = request.GET['date_from']
        date_to = request.GET['date_to']
        movie_id = request.GET['movie_id']

        # get movies from range
        top_movies = self.get_queryset().filter(
            date__range=(date_from, date_to))
        # aggregate to get No. of comments and rank


        # Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3),
        #                       headline='Hello')

        # person_list = list(map(lambda t: t[0:2],
        #                        draws.filter(drawed=False).exclude(
        #                            person=buyer).values_list()))
        top = self.get_queryset().order_by('id').last()
        serializer = self.get_serializer_class()(top)
        return Response(serializer.data)