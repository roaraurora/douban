# -*- coding: utf-8 -*-
# @File  : movie_service.py
# @Author: deeeeeeeee
# @Date  : 2018/7/3
from project.main import db
from project.main.model.movie import Movie
from flask import jsonify


def get_a_movie(id):
    return Movie.query.filter_by(id=id).first()


def delete_a_movie(id):
    movie = Movie.query.filter_by(id=id).first()
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return {
                   'status': 'success',
                   'message': 'delete movie success'
               }, 204
    else:
        return {
                   'status': 'fail',
                   'message': 'movie not find'
               }, 404


def get_movie_order(page: int, per_page: int):
    return Movie.query.order_by(Movie.rank).paginate(page, per_page, error_out=False)


def get_movie_by_query(query_string: str, page: int, per_page: int):
    return Movie.query.filter(Movie.category.like("%{}%".format(query_string))).paginate(page, per_page,
                                                                                         error_out=False)


def get_movie_bt_search(search_pattern: str, page: int, per_page: int):
    return Movie.query.filter(Movie.name.like("%{}%".format(search_pattern))).paginate(page, per_page,
                                                                                       error_out=False)
