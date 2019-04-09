from rest_framework import viewsets
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import pdb
from django.db.models import Count
from .utils import get_date
from ranking import Ranking


class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # def create(self, request, *args, **kwargs):
    #     write_serializer = MovieSerializer(data=request.data)
    #     write_serializer.is_valid(raise_exception=True)
    #     # instance = self.perform_create(write_serializer)
    #
    #     instance = self.queryset.filter(movie_title=write_serializer.data['movie_title'])
    #     read_serializer = MovieSerializer(instance)
    #     pdb.set_trace()
    #     return Response(read_serializer.data)


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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
