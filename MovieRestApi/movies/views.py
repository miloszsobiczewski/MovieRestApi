from rest_framework import viewsets
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer
from rest_framework.response import Response
from django.db import connection
from ranking import Ranking, DENSE
import datetime


class MovieView(viewsets.ModelViewSet):
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):

        write_serializer = MovieSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)

        self.perform_create(write_serializer)

        res = write_serializer.data
        movie = Movie.objects.all().filter(id=res['id'])
        res.update(movie.values('omdb_details')[0])

        return Response(res)

    def get_queryset(self):
        """

        """
        queryset = Movie.objects.all()

        # title filter
        movie_title = self.request.query_params.get('movie_title', None)
        if movie_title is not None:
            queryset = queryset.filter(movie_title=movie_title)

        # year filter
        year = self.request.query_params.get('year', None)
        if year is not None:
            year_filter = 'Year\': \'%s' % year
            pk_list = queryset.values_list('pk', flat=True).filter(
                omdb_details__contains=year_filter)
            queryset = queryset.filter(pk__in=pk_list)

        # genre filter
        genre = self.request.query_params.get('genre', None)
        if genre is not None:
            genre_regex = "Genre\'\:\ \'.*%s" % genre
            pk_list = queryset.values_list('pk', flat=True).filter(
                omdb_details__iregex=genre_regex)
            queryset = queryset.filter(pk__in=pk_list)

        # pdb.set_trace()

        return queryset


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned comments to a given movie,
        by filtering against a `movie_id` query parameter in the URL.
        """
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is not None:
            queryset = queryset.filter(movie_id=movie_id)
        return queryset


class TopView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request):
        try:
            date_from = request.GET.get('date_from', '2.1.1410')
            date_from = datetime.datetime.strptime(date_from, '%d.%m.%Y')
        except ValueError:
            date_from = datetime.date(1410, 8, 15)

        date_from -= datetime.timedelta(days=1)

        try:
            date_to = request.GET.get('date_to', '31.12.9999')
            date_to = datetime.datetime.strptime(date_to, '%d.%m.%Y')
        except ValueError:
            date_from = datetime.date(9999, 12, 31)

        # cmnt = Movie.objects.filter(
        #     Q(comment__date__range=(date_from, date_to)) |
        #     Q(comment__date__isnull=True)).values("id").annotate(
        #     total_comments=Count("comment")).order_by('-total_comments')

        # SQL STMT that can do all above and adds 0 for movies with no comments
        # but much easier
        sql_qry = \
            'SELECT "movies_movie"."id" AS "movie_id", ' \
            'SUM(CASE WHEN "movies_comment"."date" ' \
                'BETWEEN datetime("%s") AND datetime("%s") ' \
                'THEN 1 ELSE 0 end) as "total_comments" ' \
            'FROM "movies_movie" LEFT OUTER JOIN "movies_comment" ' \
            'ON ("movies_movie"."id" = "movies_comment"."movie_id_id") ' \
            'GROUP BY "movies_movie"."id" ' \
            'ORDER BY "total_comments" DESC' % (date_from, date_to)

        with connection.cursor() as c:
            c.execute(sql_qry)

            "Return all rows from a cursor as a dict"
            columns = [col[0] for col in c.description]
            cmnt = [dict(zip(columns, row)) for row in c.fetchall()]

        # add rank
        total_comments = [c['total_comments'] for c in cmnt]
        ranked_comments = list(Ranking(total_comments, strategy=DENSE))
        for i in range(len(cmnt)):
            cmnt[i]['rank'] = ranked_comments[i][0] + 1

        return Response(cmnt)
