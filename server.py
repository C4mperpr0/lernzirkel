from flask import *
from flask_socketio import SocketIO
import json
import os

from serverconfig import Serverconfig
from flask_session import Session
import database

import accounts
import student
import timetable
import docs

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

app = Flask(__name__)

database.init_app(app)

app.config['SECRET_KEY'] = Serverconfig.config['session_secret_key']
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False,
                    cors_allowed_origins='*')  # cors_allowed_origins='*' is for session access

app.register_blueprint(docs.docs.docs, url_prefix="/docs")
app.register_blueprint(accounts.login.login, url_prefix="/login")
app.register_blueprint(accounts.register.register, url_prefix="/register")
app.register_blueprint(accounts.verify.verify, url_prefix="/verify")
app.register_blueprint(student.add.studentAdd, url_prefix="/student/add")
app.register_blueprint(student.list.studentList, url_prefix="/student/list")
app.register_blueprint(timetable.add.timetableAdd, url_prefix="/timetable/add")
app.register_blueprint(timetable.list.timetableList, url_prefix="/timetable/list")
socketio.on_namespace(student.list.Socketio('/student/list'))
socketio.on_namespace(timetable.list.Socketio('/timetable/list'))


@app.route('/loginred')
def loginred():
    return '<html><body> <form action="../login", method="GET"> <input tpye="text", name="redirect"/> <input type="submit" value="submit" /> </form> </body></html>'

# URL NOT WORKING FIX LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.route('/help')
def help():
    print("help")
    return redirect("/docs")

# URL NOT WORKING FIX LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.route('/hilfe')
def hilfe():
    return redirect("/docs")


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    socketio.run(app,
                 port=Serverconfig.config['server_port'],
                 host=Serverconfig.config['server_ip'],
                 debug=Serverconfig.config['debug'])  # threaded=Serverconfig.config['threading'])
