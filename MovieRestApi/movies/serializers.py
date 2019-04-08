from rest_framework import serializers
from .models import Movie, Comment
import requests as r
import pdb

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'movie_title')

    def create(self, validated_data):
        instance = Movie.objects.create(**validated_data)

        movie_title = instance.movie_title

        # get external movie data from OMDb API
        api_key = '120e2295'
        url = 'http://www.omdbapi.com/?t=%s&apikey=%s' % (movie_title, api_key)
        print(url)
        response = r.get(url)
        if response.status_code == '200':
            print('OK')
        else:
            print('Not OK')

        data = response.json()
        print(data)
        pdb.set_trace()

        instance.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'comment_txt', 'date')

