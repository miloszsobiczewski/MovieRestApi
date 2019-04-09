from rest_framework import viewsets
from .models import Movie, Comment
from .serializers import MovieSerializer, MovieSerializerOutput
from .serializers import CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import pdb
from django.db.models import Count
from .utils import get_date
from ranking import Ranking


class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        write_serializer = MovieSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        self.perform_create(write_serializer)

        res = write_serializer.data
        movie = Movie.objects.all().filter(id=res['id'])
        res.update(movie.values('omdb_details')[0])

        return Response(res)


class CommentView(viewsets.ModelViewSet):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is not None:
            queryset = queryset.filter(movie_id=movie_id)
        return queryset

    @action(methods=['GET'], detail=False)
    def top(self, request):
        date_from = get_date(request.GET['date_from'])
        date_to = get_date(request.GET['date_to'])

        cmnt = Comment.objects.filter(
            date__range=(date_from, date_to)).values('movie_id').annotate(
            total_comments=Count('comment_txt')).order_by('-total_comments')

        # add rank
        total_comments = [c['total_comments'] for c in cmnt]
        ranked_comments = list(Ranking(total_comments))
        for i in range(0, len(cmnt)):
            cmnt[i]['rank'] = ranked_comments[i][0] + 1

        # top = self.get_queryset().order_by('id').last()
        # serializer = self.get_serializer_class()(cmnt)
        return Response(cmnt)
