from flask import *
import json
import time
from sqlalchemy import desc
from datetime import datetime

from serverconfig import Serverconfig


Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

timetableAdd = Blueprint("timetableAdd", __name__, static_folder="static", template_folder="templates")


@timetableAdd.route('/', methods=['GET', 'POST'])
def timetableAdd_():
    if request.method == 'POST':
        time.sleep(1)
        print(request.form)
        # check for errors
        # if request.form['forename'] == '':
        #     return jsonify({'error': 'err00'})  # forename empty
        # elif request.form['surname'] == '':
        #     return jsonify({'error': 'err10'})  # surname empty
        # elif request.form['school'] == '':
        #     return jsonify({'error': 'err20'})  # school empty
        # elif request.form['grade'] == '':
        #     return jsonify({'error': 'err30'})  # grade empty
        if request.form['processtype'] == 'add_date':
            timetable_id = current_app.DbClasses.Timetable.query.order_by(desc(current_app.DbClasses.Timetable.id)).first()
            current_app.db.session.add(current_app.DbClasses.Timetable(id=1+timetable_id.id if timetable_id is not None else 0,
                                                                       student=request.form["student"],
                                                                       teacher=request.form["teacher"],
                                                                       date=datetime.strptime(request.form["date"], '%Y-%m-%d'))) # '%d/%m/%y %H:%M:%S'
        else:
            timetable_regular_id = current_app.DbClasses.TimetableRegular.query.order_by(asc(current_app.DbClasses.TimetableRegular.id)).first()
            current_app.db.session.add(current_app.DbClasses.TimetableRegular(id=1+timetable_regular_id.id if timetable_regular_id is not None else 0,
                                                                              student=request.form["student"],
                                                                              teacher=request.form["teacher"],
                                                                              day=request.form["day"]))
        
        current_app.db.session.commit()

        return jsonify({'visiturl': '/timetable/list'})

    else:
        return render_template('timetable/add.html',
                               all_teachers=current_app.DbClasses.Teacher.query.order_by(current_app.DbClasses.Teacher.surname).all(),
                               teacher_logedin_id=session['teacher_id'],
                               **colorThemes['default'])
