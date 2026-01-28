from django.db import models
from django.contrib.auth.models import User
from movies.models import Film

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")  # 👈 empêche doublons par utilisateur

    def __str__(self):
        return self.name


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="items")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="playlist_items")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("playlist", "film")  # empêche doublons

    def __str__(self):
        return f"{self.playlist.name} → {self.film.titre}"


class WatchLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_later")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="watch_later_items",null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film')  # empêche doublons

    def __str__(self):
        return f"{self.user.username} → {self.film.titre}"
