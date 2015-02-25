#!/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from pyramid.config import Configurator


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # Load configurations
    from ocscacicserver.model import initialize_sql

    initialize_sql(settings)
    config = Configurator(settings=settings)
    config.scan('ocscacicserver.model')  # the "important" line

    from ocscacicserver.config.routing import make_routes

    make_routes(config)
    config.scan('ocscacicserver')

    return config.make_wsgi_app()