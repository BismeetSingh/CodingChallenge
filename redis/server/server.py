from typing import Any
import tornado
import argparse
import logging
import  shelve
from parsers.resp_parser import RespParser
from tornado.httputil import HTTPServerRequest
from tornado.web import Application


class RedisHandler(tornado.web.RequestHandler):

    def __init__(self, application: Application, request: HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        print('Parser started')
        self.application = application
        self.parser = RespParser()

    def write_to_cache(self, key, value):
        self.application.cache[key] = value

    def get_from_cache(self, key):
        return self.application.cache.get(key)

    def post(self):
        pass


def make_app():
    from server.ping_handler import PingHandler
    from server.echo_handler import EchoHandler
    from server.redis_dict_handler import RedisDictHandler
    # from ping_handler import PingHandler
    # from echo_handler import EchoHandler
    # from redis_dict_handler import RedisDictHandler
    application =  tornado.web.Application([
        (r"/ping", PingHandler),
        (r"/echo", EchoHandler),
        (r"/set", RedisDictHandler),
        (r"/get", RedisDictHandler),

    ])
    application.cache = {}
    return  application


def main():
    app = make_app()
    app.listen(6389)
    parser = argparse.ArgumentParser(description='A Redis Client')
    parser.add_argument("--PING", action='store_true')
    parser.add_argument("--ECHO", action='store_true')
    args = parser.parse_args()
    if args.PING:
        pass
    if args.ECHO:
        pass
    logging.getLogger().setLevel(logging.DEBUG)
    print('Server started')
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
