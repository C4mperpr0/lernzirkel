from flask import *
from flask_socketio import Namespace, emit
import json
import time
import datetime

from serverconfig import Serverconfig

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

dashboard = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")


@dashboard.route('/', methods=['GET', 'POST'])
def dashboard_():
    if request.method == 'GET':
        if 'teacher_id' not in session.keys():
            return f"Sie sind nicht angemeldet! Klicken sie <a href={url_for('login.login_')}>hier</a> um sich anzumelden."
        return render_template('teacher/dashboard.html',
                               **colorThemes['default'])


# socket_io
class Socketio(Namespace):
    def on_fetch_today(self):

        start_day = datetime.datetime.now()
        end_day = start_day + datetime.timedelta(days=1)

        data = current_app.DbClasses.Timetable.query.filter(current_app.DbClasses.Timetable.date.between(f"{start_day.year}-{start_day.month:02}-{start_day.day:02}", f"{end_day.year}-{end_day.month:02}-{end_day.day:02}")).order_by(current_app.DbClasses.Timetable.date.asc()).all()

        print(data)
        """
        data2 = current_app.DbClasses.TimetableRegular.query.all()
        print("---------DATA2 --------")
        print(len(data))
        print(len(data2))
        #print([t.as_timetable(int(query['year']), int(query['month']), date_as_json=True) for t in data2] if len(data2) != 0 else [])
        timetable_from_regular = []
        for t in data2:
            tlist/metable_from_regular += t.as_timetable(int(query['year']), int(query['month']), date_as_json=True)
        print("---------DATA2 end ----")
        """
        
        emit('update', {'data': ([t.as_dict(date_as_json=True) for t in data] if len(data) != 0 else [])})

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


