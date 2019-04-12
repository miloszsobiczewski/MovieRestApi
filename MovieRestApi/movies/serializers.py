from rest_framework import serializers
from .models import Movie, Comment
from . import utils as ut


def validate_movie_existence(value):

    movie_title = value['movie_title']
    data = ut.get_omdb_data(movie_title)

    if data['Response'] == 'False':
        raise serializers.ValidationError(
            "This movie doesn\'t exist in OMDb.")
    return value


class MovieSerializer(serializers.ModelSerializer):
    omdb_details = serializers.CharField(read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'movie_title', 'omdb_details')
        validators = [
            validate_movie_existence
        ]

    def create(self, validated_data):

        instance = Movie.objects.create(**validated_data)
        movie_title = instance.movie_title

        data = ut.get_omdb_data(movie_title)

        instance.omdb_details = data
        instance.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'comment_txt', 'date')

