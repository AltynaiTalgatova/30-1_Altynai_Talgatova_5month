from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, \
    DirectorValidateSerializer, MovieValidateSerializer, ReviewValidateSerializer
from movie_app.models import Director, Movie, Review


@api_view(['GET', 'POST'])
def director_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(instance=directors, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})

        name = serializer.validated_data.get('name')
        director = Director.objects.create(name=name)
        director.save()
        return Response(data=DirectorSerializer(director).data)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, director_id):
    try:
        director = Director.objects.get(id=director_id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(instance=director, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'The director has been removed.'})
    elif request.method == 'PUT':
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(data=DirectorSerializer(director).data)


@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        # Step 1 Collect all data from DB (Queryset)
        movies = Movie.objects.select_related('director').prefetch_related('reviews').all()
        # Step 2 Reformat queryset to Dictionary
        data = MovieSerializer(instance=movies, many=True).data
        # Step 3 Return Json data
        return Response(data=data)
    elif request.method == 'POST':
        # Step 0 Validation
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        # Step 1 Get data from validated data
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')
        # Step 2 Create movie
        movie = Movie.objects.create(title=title, description=description,
                                     duration=duration, director_id=director_id)
        movie.save()
        # Step 3 Return created object
        return Response(data=MovieSerializer(movie).data)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(instance=movie, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'The movie has been removed'})
    elif request.method == 'PUT':
        # Validation
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
        movie.save()
        return Response(data=MovieSerializer(movie).data)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(instance=reviews, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})

        text = serializer.validated_data.get('text')
        movie_id = serializer.validated_data.get('movie_id')
        stars = serializer.validated_data.get('stars')
        review = Review.objects.create(text=text, movie_id=movie_id, stars=stars)
        review.save()
        return Response(data=ReviewSerializer(review).data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(instance=review, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'Review has been removed'})
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.save()
        return Response(data=ReviewSerializer(review).data)


"""Generic's and Mixin's"""


class DirectorListCreateAPIView(ListCreateAPIView):     # GET, POST
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        """Create instance of Product"""
        director = Director.objects.create(
            name=serializer.validated_data.get('name'),
        )
        return Response(data=self.serializer_class(director, many=False).data,
                        status=status.HTTP_201_CREATED)


class DirectorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):     # GET, PUT, DELETE
    serializer_class = DirectorSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = self.get_object()

        obj.name = serializer.validated_data.get('name')
        obj.save()

        return Response(data=self.serializer_class(obj, many=False).data,
                        status=status.HTTP_200_OK)


class MovieViewSet(ModelViewSet):     # GET, POST, GET, PUT, DELETE
    queryset = Movie.objects.select_related('director').prefetch_related('reviews').all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        """Create instance of Movie"""
        movie = Movie.objects.create(
            title=serializer.validated_data.get('title'),
            description=serializer.validated_data.get('description'),
            duration=serializer.validated_data.get('duration'),
            director_id=serializer.validated_data.get('director_id'),
        )
        return Response(data=self.serializer_class(movie, many=False).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = self.get_object()

        obj.title = serializer.validated_data.get('title')
        obj.description = serializer.validated_data.get('description')
        obj.duration = serializer.validated_data.get('duration')
        obj.director_id = serializer.validated_data.get('director_id')
        obj.save()

        return Response(data=self.serializer_class(obj, many=False).data,
                        status=status.HTTP_200_OK)


class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        """Create instance of Review"""
        review = Review.objects.create(
            text=serializer.validated_data.get('text'),
            stars=serializer.validated_data.get('stars'),
            movie_id=serializer.validated_data.get('movie_id'),
        )
        return Response(data=self.serializer_class(review, many=False).data,
                        status=status.HTTP_201_CREATED)


class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = self.get_object()

        obj.text = serializer.validated_data.get('text')
        obj.stars = serializer.validated_data.get('stars')
        obj.movie_id = serializer.validated_data.get('movie_id')
        obj.save()

        return Response(data=self.serializer_class(obj, many=False).data,
                        status=status.HTTP_200_OK)
