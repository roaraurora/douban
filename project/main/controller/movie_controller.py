from flask import request
from flask_restplus import Resource
from ..util.parser import pagination_arguments

from ..util.dto import MovieDto
from ..model.movie import Movie

api = MovieDto.api
_page_of_movie = MovieDto.page_of_movie


@api.route('/')
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
        page = args.get('page', 1)
        per_page = args.get('per_page', 16)
        movie_page = Movie.query.paginate(page, per_page, error_out=False)
        return movie_page
