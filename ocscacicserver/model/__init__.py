#!/bin/env python
# -*- coding: utf-8 -*-
# from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import create_engine


def initialize_sql(settings):

    global DBSession
    global sqlalchemy_url
    global DBSession
    global engine
    global Session
    global session
    global tmp_dir

    # Sessão do SQLAlchemy
    sqlalchemy_url = settings['sqlalchemy.url']
    DBSession = scoped_session(sessionmaker())
    engine = create_engine(sqlalchemy_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    DBSession.configure(bind=engine)

    # Configurações genéricas
    tmp_dir = settings['tmp_dir']