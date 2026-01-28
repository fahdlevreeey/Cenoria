from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Film
from interactions.models import Note
from interactions.forms import NoteForm
from django.db.models import Q
from playlists.models import WatchLater, Playlist


@login_required
def dashboard(request):
    query = request.GET.get("q", "")
    films = Film.objects.all()

    if query:
        films = films.filter(
            Q(titre__icontains=query) |
            Q(description__icontains=query) |
            Q(genre__icontains=query)
        )

    films = films.order_by('-date_sortie')

    # IDs des films Watch Later pour l'utilisateur
    watch_later_ids = request.user.watch_later.all().values_list('film_id', flat=True)
    watch_later_items = WatchLater.objects.filter(user=request.user).select_related("film")

    context = {
    "films": films,
    "query": query,
    "watch_later_ids": watch_later_ids,
    "watch_later_items": watch_later_items,  
    }


    return render(request, "movies/dashboard.html", context)

@login_required
def film_detail(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    recommandations = film.get_recommendations()

    # Watch Later pour le bouton
    watch_later_ids = request.user.watch_later.all().values_list('film_id', flat=True)
    playlists = Playlist.objects.filter(user=request.user) if request.user.is_authenticated else []


    # Gestion notation utilisateur
    note_existante = Note.objects.filter(utilisateur=request.user, film=film).first()

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note_existante)
        if form.is_valid():
            note = form.save(commit=False)
            note.utilisateur = request.user
            note.film = film
            note.save()
    else:
        form = NoteForm(instance=note_existante)

    context = {
        "film": film,
        "recommandations": recommandations,
        "form": form,
        "note_user": note_existante,
        "watch_later_ids": watch_later_ids,
        "playlists": playlists,
    }
    return render(request, "movies/film_detail.html", context)
