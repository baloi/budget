from datetime import datetime
from datetime import timedelta

from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, Text, Numeric
from sqlalchemy.orm import synonym
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

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

class Transaction(Base):
  """An item (expense or earning)."""
  __tablename__ = 'transaction'

  id = Column(Integer, primary_key=True)

  # TODO: created should be changed to date with "date" value and today as 
  # default
  created = Column(DateTime, default = datetime.now)
  name = Column(String(255))
  description = Column(Text)
  # ForeignKey: item.id
  item_id = Column(Integer, ForeignKey('item.id'))

  amount = Column(Numeric(10, 2))
  type = Column(String(20))

  __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'transaction'
  }

  def repr():
    return (u'<{self.__class__.__name__): {self.id}>'.format(self=self))

class Expense(Transaction):
  __mapper_args__ = {
    'polymorphic_identity':'expense'
  }

  # Relationship: An Expense is a payment to an item. An Item can have one to 
  # many payments
  #item = relationship("Item", backref=backref('payments', order_by=id))

class Earning(Transaction):
  __mapper_args__ = {
    'polymorphic_identity':'earning'
  }


class Item(Base):
  """An item bought or to buy."""
  __tablename__ = 'item'

  id = Column(Integer, primary_key=True)
  created = Column(DateTime, default = datetime.now)
  modified = Column(DateTime, default = datetime.now, onupdate=datetime.now)
  name = Column(String(255))
  done = Column(Boolean, default=False)
  description = Column(Text)

  amount = Column(Numeric(10, 2))

  # Relationship: Item has one to many payments, a payment being an Expense
  payments = relationship("Expense", order_by="Expense.id", backref="item")

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
