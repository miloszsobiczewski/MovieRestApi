from django.shortcuts import render
from rest_framework import viewsets
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import pdb
from django.db.models import Avg, Count, Min, Sum, Max
import datetime
from .utils import get_date


class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(methods=['GET'], detail=False)
    def top(self, request):
        date_from = get_date(request.GET['date_from'])
        date_to = get_date(request.GET['date_to'])

        # get movies from range
        # top_movies = self.get_queryset().filter(
        #     date__range=(date_from, date_to))
        # aggregate to get No. of comments
        cmnt = Comment.objects.filter(
            date__range=(date_from, date_to)).values('movie_id').annotate(
            total_comments=Count('comment_txt')).order_by('-total_comments')

        # add rank
        max_cnt = cmnt[0]['total_comments']
        for i in range(0, len(cmnt)):
            cmnt[i]['rank'] = max_cnt - cmnt[i]['total_comments'] + 1
        
        # top = self.get_queryset().order_by('id').last()
        # serializer = self.get_serializer_class()(cmnt)

        # pdb.set_trace()

        return Response(cmnt)
