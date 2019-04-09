from rest_framework import serializers
from .models import Movie, Comment
import requests as r
from rest_framework.validators import UniqueValidator
import pdb
import json


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'movie_title')

    def create(self, validated_data):

        instance = Movie.objects.create(**validated_data)
        movie_title = instance.movie_title

        # read config data
        with open("movies/config.JSON") as config_file:
            conf = json.load(config_file)

        # get external movie data from OMDb API
        url = conf['api_url'] % (movie_title, conf['api_key'])
        print(url)

        # check for response code
        response = r.get(url)
        if response.status_code == '200':
            print('OK')
        else:
            print('Not OK')

        data = response.json()
        print(data)
        # pdb.set_trace()

        instance.omdb_details = data
        instance.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'comment_txt', 'date')

