from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Playlist, PlaylistItem, WatchLater

@login_required
def playlists_list(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, "playlists/list.html", {"playlists": playlists})


@login_required
def create_playlist(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Playlist.objects.create(user=request.user, name=name)
        return redirect("playlists_list")
    return render(request, "playlists/create.html")


@login_required
def add_to_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    if request.method == "POST":
        title = request.POST.get("title")
        PlaylistItem.objects.create(playlist=playlist, title=title)
    return redirect("playlists_list")


@login_required
def remove_from_playlist(request, item_id):
    item = get_object_or_404(PlaylistItem, id=item_id, playlist__user=request.user)
    item.delete()
    return redirect("playlists_list")


@login_required
def watch_later(request):
    items = WatchLater.objects.filter(user=request.user)
    return render(request, "playlists/watch_later.html", {"items": items})


@login_required
def add_watch_later(request):
    if request.method == "POST":
        title = request.POST.get("title")
        WatchLater.objects.create(user=request.user, title=title)
    return redirect("watch_later")


@login_required
def remove_watch_later(request, item_id):
    item = get_object_or_404(WatchLater, id=item_id, user=request.user)
    item.delete()
    return redirect("watch_later")
