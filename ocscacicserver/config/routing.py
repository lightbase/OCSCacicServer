#!/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from ocscacicserver.view.restfulview import viewcoleta


def make_routes(config):
    """
    Cria rotas
    """
    config.add_route('the_big_colect', 'rest/coleta', request_method='GET')
    config.add_view(view=viewcoleta, route_name='the_big_colect', request_method='GET')
