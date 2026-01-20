from django.contrib import admin

from .models import Film


class FilmAdmin(admin.ModelAdmin):
    # On veut voir le TITRE, le GENRE, et la MOYENNE
    list_display = ("titre", "genre", "get_moyenne", "apercu_recommendations")

    def apercu_recommendations(self, obj):

        recommendations = obj.get_recommendations()

        return [f.titre for f in recommendations]


# On enregistre le Film avec cette configuration
admin.site.register(Film, FilmAdmin)
