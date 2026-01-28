from django.urls import path
from . import views

app_name = "movies"


urlpatterns = [

path("dashboard/", views.dashboard, name="dashboard"),
path("film/<int:film_id>/", views.film_detail, name="film_detail"),
path('categories/<str:category_code>/', views.category_films, name='category_films'),
path('categories/', views.categories_overview, name='categories_overview'),

]