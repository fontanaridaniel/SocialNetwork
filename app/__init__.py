from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_login import LoginManager, logout_user, login_required

app = Flask(__name__, static_url_path='/app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "adlfhblajkedmòdsfhdisayuflsdugadsckseiyfcdan"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['IMAGINE_FILTER_SETS'] = {
    'filter_set_name': {
        'filters': {
            'autorotate': {}
        }
    }
}
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
socketio = SocketIO(app, async_mode="threading")

from app import routes