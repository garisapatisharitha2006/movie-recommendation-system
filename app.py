from flask import Flask, render_template, request, redirect
from extensions import db
from models import User, Movie
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(username=request.form["username"], password=request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("register.html")


@app.route("/dashboard")
@login_required
def dashboard():
    search = request.args.get("search")
    language = request.args.get("language")
    genre = request.args.get("genre")

    query = Movie.query

    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))
    if language:
        query = query.filter_by(language=language)
    if genre:
        query = query.filter_by(genre=genre)

    movies = query.all()

    # Recommendation based on preference
    recommended = Movie.query.filter_by(
        language=current_user.preferred_language or "English"
    ).limit(10).all()

    return render_template("dashboard.html", movies=movies, recommended=recommended)


@app.route("/add/<int:id>")
@login_required
def add(id):
    movie = db.session.get(Movie, id)
    if movie not in current_user.movies:
        current_user.movies.append(movie)
        db.session.commit()
    return redirect("/dashboard")


@app.route("/remove/<int:id>")
@login_required
def remove(id):
    movie = db.session.get(Movie, id)
    if movie in current_user.movies:
        current_user.movies.remove(movie)
        db.session.commit()
    return redirect("/dashboard")


@app.route("/save_preferences", methods=["POST"])
@login_required
def save_preferences():
    current_user.preferred_language = request.form.get("language")
    current_user.preferred_genre = request.form.get("genre")
    db.session.commit()
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)