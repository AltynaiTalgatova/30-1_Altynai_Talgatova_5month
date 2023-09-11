"""
URL configuration for Afisha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from movie_app import views as movies_views
from users import views as users_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', movies_views.director_list_api_view),
    path('api/v1/directors/', movies_views.director_list_api_view),
    path('api/v1/directors/<int:director_id>/', movies_views.director_detail_api_view),
    path('api/v1/movies/', movies_views.movie_list_api_view),
    path('api/v1/movies/<int:movie_id>/', movies_views.movie_detail_api_view),
    path('api/v1/reviews/', movies_views.review_list_api_view),
    path('api/v1/reviews/<int:review_id>/', movies_views.review_detail_api_view),

    path('api/v1/users/auth/', users_views.auth_api_view),
    path('api/v1/users/register/', users_views.register_api_view),

    path('api/v1/directors_cbv/', movies_views.DirectorListCreateAPIView.as_view()),
    path('api/v1/directors_cbv/<int:id>/', movies_views.DirectorRetrieveUpdateDestroyAPIView.as_view()),
    path('api/v1/movies_cbv/', movies_views.MovieViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/v1/movies_cbv/<int:id>/', movies_views.MovieViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
    )),
    path('api/v1/reviews_cbv/', movies_views.ReviewListCreateAPIView.as_view()),
    path('api/v1/reviews_cbv/<int:id>/', movies_views.ReviewRetrieveUpdateDestroyAPIView.as_view()),
]
