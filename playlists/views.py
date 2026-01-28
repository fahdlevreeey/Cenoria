from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Playlist, PlaylistItem, WatchLater
from movies.models import Film
from django.db import IntegrityError

@login_required
def playlists_list(request):
    playlists = Playlist.objects.filter(user=request.user).prefetch_related("items__film")
    return render(request, "playlists/list.html", {"playlists": playlists})

@login_required
def create_playlist(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            try:
                Playlist.objects.create(user=request.user, name=name)
            except IntegrityError:
                pass  # playlist déjà existante → on ignore

    return redirect("playlists:playlists_list")
@login_required
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)

    if request.method == "POST":
        playlist.delete()

    return redirect("playlists:playlists_list")


@login_required
def add_to_playlist(request, playlist_id, film_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    film = get_object_or_404(Film, id=film_id)

    if request.method == "POST":
        PlaylistItem.objects.get_or_create(
            playlist=playlist,
            film=film
        )

    return redirect("movies:film_detail", film_id=film.id)


@login_required
def remove_from_playlist(request, item_id):
    item = get_object_or_404(PlaylistItem, id=item_id, playlist__user=request.user)
    item.delete()
    return redirect("playlists:playlists_list")



def watch_later(request):
    items = WatchLater.objects.filter(user=request.user).select_related("film")
    return render(request, "playlists/watch_later.html", {"items": items})

@login_required
def add_watch_later(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    WatchLater.objects.get_or_create(user=request.user, film=film)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_watch_later(request, film_id):
    item = get_object_or_404(WatchLater, user=request.user, film_id=film_id)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))