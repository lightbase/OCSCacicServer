#!/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from pyramid.config import Configurator
from .view.restfulview import viewcoleta


def main(**settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # Load configurations
    from ocscacicserver.model import initialize_sql
    initialize_sql(settings)
    config = Configurator(settings=settings)

    # Load model
    config.scan('wscserver.model')  # the "important" line

    # Rotas
    config.add_route('the_big_colect', 'rest/coleta', request_method='GET')
    config.add_view(view=viewcoleta, route_name='the_big_colect', request_method='GET')
    config.enable_POST_tunneling()

    config.scan('ocscacicserver')

    return config.make_wsgi_app()