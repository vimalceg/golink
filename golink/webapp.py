# Copyright 2018 David Coles <coles.david@gmail.com>
# This project is licensed under the terms of the MIT license. See LICENSE.txt
import argparse
import logging
import pkg_resources
import threading
from aiohttp import web
import aiohttp_jinja2
import jinja2

from golink import views, auth, sqlite, mongodb


def connect_to_database(type, connection_string):
    logging.info('Connecting to %s: %s', type, connection_string)
    if type == "sqlite":
        return sqlite.Database.connect(connection_string,threading.current_thread())
    elif type == "mongodb":
        return mongodb.Database.connect(connection_string)
    else:
        raise RuntimeError(f'Unknown connection type: {type}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='localhost')
    parser.add_argument('-P', '--port', type=int, default=8080)
    parser.add_argument('--database-type', default='sqlite')
    parser.add_argument('--database', default=':memory:')
    parser.add_argument('--auth', default='null')
    parser.add_argument('--readonly', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    app = web.Application()
    app['DATABASE'] = connect_to_database(args.database_type, args.database)
    app['AUTH_TYPE'] = auth.AUTHENTICATORS[args.auth]
    app['READONLY'] = args.readonly
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('golink', 'templates'), trim_blocks=True, lstrip_blocks=True)
    app.router.add_static('/+static', pkg_resources.resource_filename('golink', 'static'))
    app.router.add_routes(views.routes)

    web.run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
