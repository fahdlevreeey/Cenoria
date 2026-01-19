from django.urls import path
from . import views

urlpatterns = [
    path("", views.playlists_list, name="playlists_list"),
    path("create/", views.create_playlist, name="create_playlist"),
    path("add/<int:playlist_id>/", views.add_to_playlist, name="add_to_playlist"),
    path("remove/item/<int:item_id>/", views.remove_from_playlist, name="remove_from_playlist"),

    path("watch-later/", views.watch_later, name="watch_later"),
    path("watch-later/add/", views.add_watch_later, name="add_watch_later"),
    path("watch-later/remove/<int:item_id>/", views.remove_watch_later, name="remove_watch_later"),
]
