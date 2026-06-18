from app import app
from extensions import db
from models import Movie
import random

movies = [
    ("Inception","Sci-Fi","English","inception.jpg"),
    ("Titanic","Romance","English","titanic.jpg"),
    ("Interstellar","Sci-Fi","English","interstellar.jpg"),
    ("The Dark Knight","Action","English","dark_knight.jpg"),
    ("Avengers Endgame","Action","English","endgame.jpg"),
    ("Joker","Drama","English","joker.jpg"),
    ("Frozen","Fantasy","English","frozen.jpg"),
    ("La La Land","Romance","English","lalaland.jpg"),

    ("Vikram","Action","Tamil","vikram.jpg"),
    ("Master","Action","Tamil","master.jpg"),
    ("Jai Bhim","Drama","Tamil","jaibhim.jpg"),
    ("Soorarai Pottru","Drama","Tamil","soorarai.jpg"),

    ("3 Idiots","Comedy","Hindi","3idiots.jpg"),
    ("Dangal","Drama","Hindi","dangal.jpg"),
    ("PK","Comedy","Hindi","pk.jpg"),
    ("Pathaan","Action","Hindi","pathaan.jpg"),

    ("Parasite","Thriller","Korean","parasite.jpg"),
    ("Train to Busan","Action","Korean","busan.jpg"),

    ("Your Name","Romance","Japanese","yourname.jpg"),
    ("Spirited Away","Fantasy","Japanese","spiritedaway.jpg"),
]

with app.app_context():
    db.drop_all()
    db.create_all()

    for title, genre, language, image in movies:
        db.session.add(Movie(
            title=title,
            genre=genre,
            language=language,
            rating=round(random.uniform(6,9.5),1),
            image=image
        ))

    db.session.commit()

    print("✅ Movies inserted successfully!")