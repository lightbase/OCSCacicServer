# from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import create_engine


def initialize_sql(settings):

    global DBSession
    global sqlalchemy_url
    global DBSession
    global Base
    global engine
    global Session
    global session
    global tmp_dir

    sqlalchemy_url = settings['sqlalchemy.url']
    DBSession = scoped_session(sessionmaker())
    Base = declarative_base()
    engine = create_engine(sqlalchemy_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    tmp_dir = settings['tmp_dir']

    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    # Base.metadata.create_all(engine)