import requests
from flask import *
from flask_socketio import Namespace, emit
import json
from sqlalchemy import update, asc, desc
from werkzeug.utils import secure_filename

from serverconfig import Serverconfig
Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

teacherInfo = Blueprint("teacherInfo", __name__, static_folder="static", template_folder="templates")


@teacherInfo.route('/<int:teacher_id>', methods=['GET', 'POST'])
def teacherInfo_(teacher_id):
    teacher_object = current_app.DbClasses.Teacher.query.filter(current_app.DbClasses.Teacher.id == teacher_id).one_or_none()
    return render_template('teacher/info.html',
                            teacher_id=teacher_object.id,
                            teacher_forename=teacher_object.forename,
                            teacher_surname=teacher_object.surname,
                            teacher_subjects=teacher_object.subjects,
                            teacher_mail=teacher_object.mail,
                            teacher_phone=teacher_object.phone,
                            teacher_admin=teacher_object.admin,
                            teacher_verified=teacher_object.verified,
                           **colorThemes['default'])




# socket_io
class Socketio(Namespace):
    def on_set_admin(self, query):
        if any([k not in query.keys() for k in ['value', 'id']]):
            return
        print(f"{query['id']} - {query['value']}")

        current_app.DbClasses.Teacher.query.filter_by(id=query['id']).update({'admin': query['value']})
        current_app.db.session.commit()
        emit('refresh')

    def on_set_verified(self, query):
        if any([k not in query.keys() for k in ['value', 'id']]):
            return
        current_app.DbClasses.Teacher.query.filter_by(id=query['id']).update({'verified': query['value']})
        current_app.db.session.commit()
        emit('refresh')
        
