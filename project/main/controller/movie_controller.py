from flask import request
from flask_restplus import Resource

from project.main.util.decorators import token_required
from ..util.parser import pagination_arguments, prior_search_arguments
from ..util.search import get_prior_user
from ..util.dto import MovieDto
from ..model.movie import Movie
from ..service.movie_service import get_a_movie, get_movie_order, get_movie_by_query, get_movie_bt_search, \
    delete_a_movie

api = MovieDto.api
_page_of_movie = MovieDto.page_of_movie
_detail_of_movie = MovieDto.movie_detail


@api.route('')
class MovieList(Resource):

    @api.doc('get pages of movie')
    @api.response(400, 'Input payload validation failed')
    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(_page_of_movie)
    def get(self):
        """
        :return:list of movies
        """
        args = pagination_arguments.parse_args(request)
        search = args.get('search', None)
        page = args.get('page', 1)
        per_page = args.get('per_page', 16)

        if search:
            movie_page = get_movie_bt_search(search_pattern=search, page=page, per_page=per_page)
        else:
            movie_page = get_movie_order(page, per_page)
        return movie_page


@api.route('/<int:id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'Movie not found')
class MovieById(Resource):
    @token_required
    @api.doc('get a movie')
    @api.marshal_with(_detail_of_movie, skip_none=True)  # 将user dto作为序列化的对象
    def get(self, id):
        """get a user given its identifier"""
        movie = get_a_movie(id)
        print("User by id : {}".format(movie))
        if movie:
            return movie
        else:
            api.abort(404, status='fail', message='Movie not found')

    @token_required
    @api.doc('get a movie')
    def delete(self, id):
        """delete a user given its identifier"""
        resp = delete_a_movie(id)
        return resp


@api.route('/category/<query_string>')
@api.param('query_string', 'the request query string')
class MovieListByQuery(Resource):

    @api.doc('get pages of movie by query')
    @api.response(400, 'Input payload validation failed')
    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(_page_of_movie)
    def get(self, query_string):
        """
        :return:list of movies by category age:[198,199,200,201] area:[美国,日本,英国,法国...etc] class:[犯罪,剧情,动画]
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 16)
        movie_page = get_movie_by_query(query_string, page, per_page)
        return movie_page


@api.route('/name')
class MovieSearchPrior(Resource):

    @api.doc('get movie name by prior search')
    @api.expect(prior_search_arguments, validate=True)
    @api.response(404, 'request args value cant be null')
    def get(self):
        args = prior_search_arguments.parse_args(request)
        search_string = args.get('search', None)
        if search_string:
            return get_prior_user(search_string)
        api.abort(404, status='fail', message='Prior search Movie not found')
