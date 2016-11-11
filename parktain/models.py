
# Standard library
from os.path import abspath, dirname, join

# 3rd-party library
from sqlalchemy import Column, String, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base


HERE = dirname(abspath(__file__))
engine = create_engine('sqlite:///{}'.format(join(HERE, 'slack-archives.db')))
engine.echo = False

Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    num_members = Column(Integer, nullable=False)

    def __str__(self):
        return "<{self.id}|{self.name}>".format(**{'self': self})


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False, index=True)
    channel_id = Column(String, nullable=False, index=True)
    message = Column(String(4096))
    timestamp = Column(DateTime)

    def __str__(self):
        return "<Message(user='%s' said='%s' in channel='%s')>" % (
            self.user_id, self.message, self.channel_id)


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)

    def __str__(self):
        return "<{self.id}|{self.name}>".format(**{'self': self})
