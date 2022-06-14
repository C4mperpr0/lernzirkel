from flask import *
from flask_socketio import SocketIO
import json
import os
import datetime

from serverconfig import Serverconfig
from flask_session import Session
import database
#import backup
# DO NOT FORGET TO REACTIVATE AND IMPROVE BACKUP FUNCIONALITY

import dashboard
import teacher
import student
import timetable
import docs

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

def create_app():
    app = Flask(__name__)
    database.init_app(app)
    app.config['SECRET_KEY'] = Serverconfig.config['session_secret_key']
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    socketio = SocketIO(app, manage_session=False,
                        logger=True,
                        cors_allowed_origins='*')  # cors_allowed_origins='*' is for session access
    return app, socketio

app, socketio = create_app()

app.register_blueprint(docs.docs.docs, url_prefix="/docs")
app.register_blueprint(dashboard.dashboard.dashboard, url_prefix="/")
app.register_blueprint(teacher.add.teacherAdd, url_prefix="/teacher/add")
app.register_blueprint(teacher.list.teacherList, url_prefix="/teacher/list")
app.register_blueprint(teacher.info.teacherInfo, url_prefix="/teacher/info")
app.register_blueprint(teacher.login.login, url_prefix="/teacher/login")
app.register_blueprint(student.add.studentAdd, url_prefix="/student/add")
app.register_blueprint(student.list.studentList, url_prefix="/student/list")
app.register_blueprint(student.info.studentInfo, url_prefix="/student/info")
app.register_blueprint(timetable.add.timetableAdd, url_prefix="/timetable/add")
app.register_blueprint(timetable.list.timetableList, url_prefix="/timetable/list")
socketio.on_namespace(dashboard.dashboard.Socketio('/'))
socketio.on_namespace(teacher.list.Socketio('/teacher/list'))
socketio.on_namespace(teacher.info.Socketio('/teacher/info'))
socketio.on_namespace(student.list.Socketio('/student/list'))
socketio.on_namespace(timetable.list.Socketio('/timetable/list'))


@app.route('/loginred')
def loginred():
    return '<html><body> <form action="../login", method="GET"> <input tpye="text", name="redirect"/> <input type="submit" value="submit" /> </form> </body></html>'

@app.route('/jakob_stinkt')
def jakob_stinkt():
    return '<html><head><title>Jakob Stinkt?</title></head><body><h1>Ja es ist wahr! Jakob stinkt!</h1></body></html>'


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
