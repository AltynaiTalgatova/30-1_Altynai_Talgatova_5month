from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from .models import Director, Movie, Review


@api_view(['GET'])
def director_list_api_view(request):
    directors = Director.objects.all()
    data = DirectorSerializer(instance=directors, many=True).data
    return Response(data=data)


@api_view(['GET'])
def director_detail_api_view(request, director_id):
    try:
        director = Director.objects.get(id=director_id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = DirectorSerializer(instance=director, many=False).data
    return Response(data=data)


@api_view(['GET'])
def movie_list_api_view(request):
    movies = Movie.objects.select_related('director').prefetch_related('reviews').all()
    data = MovieSerializer(instance=movies, many=True).data
    return Response(data=data)


@api_view(['GET'])
def movie_detail_api_view(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = MovieSerializer(instance=movie, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(instance=reviews, many=True).data
    return Response(data=data)


@api_view(['GET'])
def review_detail_api_view(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(instance=review, many=False).data
    return Response(data=data)
