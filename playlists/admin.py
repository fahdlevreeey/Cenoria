from django.contrib import admin
from .models import Playlist, PlaylistItem, WatchLater

class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 1

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    inlines = [PlaylistItemInline]

@admin.register(WatchLater)
class WatchLaterAdmin(admin.ModelAdmin):
    list_display = ("film", "user", "added_at")
