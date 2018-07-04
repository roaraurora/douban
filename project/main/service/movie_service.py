# -*- coding: utf-8 -*-
# @File  : movie_service.py
# @Author: deeeeeeeee
# @Date  : 2018/7/3
from project.main import db
from project.main.model.movie import Movie


def get_a_movie(id):
    return Movie.query.filter_by(id=id).first()


def get_movie_order(page: int, per_page: int):
    return Movie.query.order_by(Movie.rank).paginate(page, per_page, error_out=False)


def get_movie_by_query(query_string: str, page: int, per_page: int):
    return Movie.query.filter(Movie.category.like("%{}%".format(query_string))).paginate(page, per_page,
                                                                                         error_out=False)


# def get_movie_query_age(query_string: str, page: int, per_page: int):
#     return Movie.query.filter(Movie.category.like("%{}%".format(query_string))).paginate(page, per_page,
#                                                                                          error_out=False)
