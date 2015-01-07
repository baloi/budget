from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from models import Base
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.secret_key=b'\x81I]\xd72.0\xa7D6\x85\xb8j\xbe7\xc9\xcf)\x88\xf7^GU\\'

from flask import abort, jsonify, redirect, render_template
from flask import request, url_for
#from forms import MessageForm
#from forms import LoginForm
#from models import Message
#from models import User

# Use Flask-SQAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and overrride its default Model class with the pure
# SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base

# Flask-Login will be loaded in request handling...
from flask import session 
#from flask.ext.login import LoginManager, current_user
#from flask.ext.login import login_user, logout_user, login_required
#login_manager = LoginManager()
#login_manager.setup_app(app)
#login_manager.login_view='login'


@app.route('/')
def index():
  #return render_template('index.html') 
  return render_template('index.html') 

if __name__=='__main__':
  #app.run()
  app.run(host='0.0.0.0', debug=True)
