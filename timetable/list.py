import requests
from flask_socketio import Namespace, emit
from flask import *
import json
import calendar
import datetime
from serverconfig import Serverconfig


Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

timetableList = Blueprint("timetableList", __name__, static_folder="static", template_folder="templates/timetable")


@timetableList.route('/', methods=['GET', 'POST'])
def timetableList_():
    return render_template('timetable/list.html',
                           **colorThemes['default'])



# socket_io
class Socketio(Namespace):
    def on_fetch(self, query):
        print(query)
        if any([k not in query.keys() for k in ['year', 'month']]):
            return
        if not query['year'].isdigit() or not query['month'].isdigit():
            return

        init_day = datetime.datetime(int(query['year']), int(query['month']), 1).strftime("%w")

        print(query)

        print(f"{query['year']}-{int(query['month']):02}-01")
        print(f"{query['year'] if int(query['month']) < 12 else int(query['year']) + 1}-{(int(query['month']) + 1 if int(query['month']) < 12 else 1):02}-01")

        data = current_app.DbClasses.Timetable.query.filter(current_app.DbClasses.Timetable.date.between(f"{query['year']}-{int(query['month']):02}-01",  f"{query['year'] if int(query['month']) < 12 else int(query['year']) + 1}-{(int(query['month']) + 1 if int(query['month']) < 12 else 1):02}-01")).order_by(current_app.DbClasses.Timetable.date.asc()).all()

        print(data)


        emit('update', {'data': [t.as_dict(date_as_string=True) for t in data] if len(data) != 0 else []})

        """
        if query['search'] != '':
            # data = current_app.DbClasses.Student.query.filter(
            #     current_app.DbClasses.Student.forename.contains(query['search']))\
            #     .join(current_app.DbClasses.Student.query.filter(
            #     current_app.DbClasses.Student.surname.contains(query['search'])), isouter=True, full=True)

            #data = current_app.DbClasses.Student.query.filter(current_app.DbClasses.Student.surname.contains(query['search']))
            #data = current_app.DbClasses.Student.query.filter(current_app.DbClasses.Student.forename.contains(query['search'])).union_all(current_app.DbClasses.Student.query.filter(current_app.DbClasses.Student.surname.contains(query['search'])))
            data = current_app.DbClasses.Student.query.filter(current_app.DbClasses.Student.surname.contains(query['search']))
        else:
            data = current_app.DbClasses.Student.query
        print(data)
        data = data.order_by((asc if query['order'] == 'asc' else desc)(query['sort']))\
            .offset(query['limit']*query['offset']).limit(query['limit']).all()
        print([s.as_dict() for s in data] if len(data) != 0 else [])
        emit('update', {'data': [s.as_dict() for s in data] if len(data) != 0 else []})
        """


