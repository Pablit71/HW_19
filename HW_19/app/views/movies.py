import json
from flask import request, jsonify
from flask_restx import Resource, Namespace
from app.database import connect, admin_required, admin_auth

from app.models import MovieSchema, Movie, User
from app.database import db

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        t = db.session.query(Movie)
        if director is not None:
            t = t.filter(Movie.director_id == director)
        if genre is not None:
            t = t.filter(Movie.genre_id == genre)
        if year is not None:
            t = t.filter(Movie.year == year)
        all_movies = t.all()
        res = movies_schema.dump(all_movies)
        return res, 201


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = Movie.query.all()
        return movies_schema.dump(all_movies), 200

    @admin_required
    def get(self):
        return "", 201

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201

    @admin_auth
    def post(self):
        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    @admin_auth
    def get(self, mid):
        try:
            movie = db.session.query(Movie).filter(Movie.id == mid).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    @admin_auth
    def put(self, mid):
        movie = db.session.query(Movie).get(mid)
        req_json = request.json

        movie.id = req_json.get("id")
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    @admin_auth
    def delete(self, mid):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204

