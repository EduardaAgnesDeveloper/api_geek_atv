from sqlmodel import create_engine, Session, SQLModel

def get_engine():
  url = 'sqlite:///teste.db'
  engine = create_engine(url)

  return engine


def sync_database(engine):
  SQLModel.metadata.create_all(engine)
