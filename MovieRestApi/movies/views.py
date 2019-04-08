from django.shortcuts import render
from rest_framework import viewsets
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer


class MovieView(viewsets.ModelViewSet):
    
