from models import Movie
import random

def get_recommendations(user):
    movies = Movie.query.all()
    watched = user.movies
    watched_ids = {m.id for m in watched}

    if not watched:
        sample = random.sample(movies, min(10, len(movies)))
        return sample, {}, sample

    genres = [m.genre for m in watched]

    scored = []

    for movie in movies:
        if movie.id in watched_ids:
            continue

        score = 1 if movie.genre in genres else 0
        scored.append((movie, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    main = [m[0] for m in scored[:10]]

    return main, {}, random.sample(movies, min(10, len(movies)))