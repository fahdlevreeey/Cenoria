from django.urls import path
from . import views

app_name = "movies"


urlpatterns = [

path("dashboard/", views.dashboard, name="dashboard"),
path("film/<int:film_id>/", views.film_detail, name="film_detail"),

]