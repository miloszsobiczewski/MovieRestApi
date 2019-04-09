from rest_framework import serializers
from .models import Movie, Comment
import requests as r
import json
import pdb


def validate_movie_existence(value):
    movie_title = value['movie_title']

    # read config data
    with open("movies/config.JSON") as config_file:
        conf = json.load(config_file)

    # get external movie data from OMDb API
    url = conf['api_url'] % (movie_title, conf['api_key'])
    print(url)
    # check response code
    response = r.get(url)
    data = response.json()
    print(data)
    if data['Response'] == 'False':
        raise serializers.ValidationError(
            "This movie doesn\'t exist in OMDb")
    return value


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'movie_title')
        validators = [
            validate_movie_existence
        ]

    def create(self, validated_data):

        instance = Movie.objects.create(**validated_data)
        movie_title = instance.movie_title

        # read config data
        with open("movies/config.JSON") as config_file:
            conf = json.load(config_file)

        # get external movie data from OMDb API
        url = conf['api_url'] % (movie_title, conf['api_key'])
        response = r.get(url)
        data = response.json()
        instance.omdb_details = data
        instance.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'comment_txt', 'date')


class TopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'comment_txt', 'date')