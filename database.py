import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata
    import models
    # drop all tables if any exists
    Base.metadata.drop_all(bind=engine)
    # craete new tables
    Base.metadata.create_all(bind=engine)
