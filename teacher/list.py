import requests
from flask_socketio import Namespace, emit
from flask import *
import json
from sqlalchemy import asc, desc

from serverconfig import Serverconfig
Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

teacherList = Blueprint("teacherList", __name__, static_folder="static", template_folder="templates")


@teacherList.route('/', methods=['GET', 'POST'])
def teacherList_():
    return render_template('teacher/list.html',
                           **colorThemes['default'])



# socket_io
class Socketio(Namespace):
    def on_fetch(self, query):
        if any([k not in query.keys() for k in ['sort', 'search', 'limit', 'offset', 'order']]):
            return
        print(query)
        if query['search'] != '':
            # data = current_app.DbClasses.Student.query.filter(
            #     current_app.DbClasses.Student.forename.contains(query['search']))\
            #     .join(current_app.DbClasses.Student.query.filter(
            #     current_app.DbClasses.Student.surname.contains(query['search'])), isouter=True, full=True)

            #data = current_app.DbClasses.Student.query.filter(current_app.DbClasses.Student.surname.contains(query['search']))
            #data = current_app.DbClasses.Student.query.filter(current_app.DbClasses.Student.forename.contains(query['search'])).union_all(current_app.DbClasses.Student.query.filter(current_app.DbClasses.Student.surname.contains(query['search'])))
            data = current_app.DbClasses.Teacher.query.filter(current_app.DbClasses.Teacher.surname.contains(query['search']))
        else:
            data = current_app.DbClasses.Teacher.query
        print(data)
        data = data.order_by((asc if query['order'] == 'asc' else desc)(query['sort']))\
            .offset(query['limit']*query['offset']).limit(query['limit']).all()
        print([s.as_dict() for s in data] if len(data) != 0 else [])
        emit('update', {'data': [s.as_dict() for s in data] if len(data) != 0 else []})
