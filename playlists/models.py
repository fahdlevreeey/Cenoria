from django.db import models
from django.contrib.auth.models import User

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=255)   # دابا غير title (ماشي movies app)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WatchLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
