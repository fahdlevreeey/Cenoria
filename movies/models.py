from django.db import models
from django.db.models import Avg  # <--- IMPORT IMPORTANT (La calculatrice)




CATEGORIES = (
    ('ACTION', 'Action'),
    ('COMEDIE', 'Comédie'),
    ('DRAME', 'Drame'),
    ('SF', 'Science-Fiction'),
    ('HORREUR', 'Horreur'),
    ('ANIMATION', 'Dessin Animé'),
)
# Create your models here.
class Film(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=50, choices=CATEGORIES)
    date_sortie = models.DateField()
    video = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/")


    def __str__(self):
        return self.titre
    
    
    def get_moyenne(self):
        resultat = self.notes.aggregate(Avg('valeur'))
        moyenne = resultat['valeur__avg']
        if moyenne is None: 
            return 0
        return round(moyenne, 1)
    

    def get_recommendations(self):
        recommendations = Film.objects.filter(genre=self.genre)
        recommendations = recommendations.exclude(id=self.id)
        return recommendations[:5]

