from werkzeug.datastructures import Headers
from flask import Response


class MyResponse(Response):
    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        # 跨域控制
        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        myheader = ('Access-Control-Allow-Headers', 'x-requested-with,content-type')
        if headers:
            headers.add(*origin)
            # headers.add(*methods)
            # headers.add(*myheader)
        else:
            # headers = Headers([origin, methods, myheader])
            headers = Headers([origin])
        kwargs['headers'] = headers
        return super().__init__(response, **kwargs)
