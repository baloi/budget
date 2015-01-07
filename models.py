from datetime import datetime
from datetime import timedelta

from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, Text, Numeric
from sqlalchemy.orm import synonym
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
  """A user login, with credentials and authentication."""
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  created = Column(DateTime, default = datetime.now)
  modified = Column(DateTime, default = datetime.now, onupdate=datetime.now)
  
  name = Column('name', String(200))
  email = Column(String(100), unique=True, nullable=False)
  active = Column(Boolean, default=True)

  _password = Column('password', String(100))

  def _get_password(self):
    return self._password

  def _set_password(self, password):
    if password:
      password = password.strip()
    self._password = generate_password_hash(password)

  # everytime user.password is set on a User instance, the password is 
  # immediately hashed using a Python descriptor and SQLAlchemy's synonym hook
  password_descriptor = property(_get_password, _set_password)
  password = synonym('_password', descriptor = password_descriptor)

  def check_password(self, password):
    if self.password is None:
      return False
    password = password.strip()
    if not password:
      return False
    return check_password_hash(self.password, password)

  @classmethod
  def authenticate(cls, query, email, password):
    email = email.strip().lower()
    user = query(cls).filter(cls.email == email).first()
    if user is None:
      return None, False
    if not user.active:
      return user, False
    return user, user.check_password(password)

  def get_id(self):
    return str(self.id)

  def is_active(self):
    return True

  def is_anonymous(self):
    return False
  
  def is_authenticated(self):
    return True

class Item(Base):
  """An item (expense or earning)."""
  __tablename__ = 'item'

  id = Column(Integer, primary_key=True)
  created = Column(DateTime, default = datetime.now)
  modified = Column(DateTime, default = datetime.now, onupdate=datetime.now)
  name = Column(String(255))
  done = Column(Boolean, default=False)
  description = Column(Text)

  amount = Column(Numeric(10, 2))

  def repr():
    return (u'<{self.__class__.__name__): {self.id}>'.format(self=self))

def get_session(create_tables=False):
  from sqlalchemy import create_engine
  from sqlalchemy.orm import sessionmaker
  engine = create_engine('sqlite:///budget.db', echo=True)

  # create session and create database tables 
  if create_tables:
    Base.metadata.create_all(engine)
  Session = sessionmaker(bind=engine)
  session = Session()
  return session


if __name__=='__main__':
  now = datetime.now()
  
  session = get_session(create_tables=True)
  item = Item(
    name = 'First Item',
    done=False,
    description='Just the first item in the list.')

  session.add(item)
  session.commit()