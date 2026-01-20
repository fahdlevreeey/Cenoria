from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from movies.models import Film


class Note(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="notes")

    # La note (Juste un chiffre simple)
    valeur = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"Note de {self.utilisateur} sur {self.film} : {self.valeur}/5"
