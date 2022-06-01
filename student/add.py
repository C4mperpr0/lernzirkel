from flask import *
import json
import time
from sqlalchemy import desc

from serverconfig import Serverconfig


Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

studentAdd = Blueprint("studentAdd", __name__, static_folder="static", template_folder="templates")


@studentAdd.route('/', methods=['GET', 'POST'])
def studentAdd_():
    if request.method == 'POST':
        time.sleep(1)
        print(request.form)

        # check for errors
        if request.form['forename'] == '':
            return jsonify({'error': 'err00'})  # forename empty
        elif request.form['surname'] == '':
            return jsonify({'error': 'err10'})  # surname empty
        elif request.form['school'] == '':
            return jsonify({'error': 'err20'})  # school empty
        elif request.form['grade'] == '':
            return jsonify({'error': 'err30'})  # grade empty


        # if problems with creation of first students (there is no highest id available) see teacher/add for fix
        student_id = int(current_app.DbClasses.Student.query.order_by(desc(current_app.DbClasses.Student.id)).first().id)
        current_app.db.session.add(current_app.DbClasses.Student(id=1+student_id if student_id is not None else 0,
                                                                 forename=request.form["forename"],
                                                                 surname=request.form["surname"],
                                                                 school=request.form["school"],
                                                                 grade=request.form["grade"].replace(' ', '').upper(),
                                                                 mail=request.form["mail"].lower(),
                                                                 phone=request.form["phone"]))
        current_app.db.session.commit()

        return jsonify({'visiturl': '/student/list'})

    else:
        return render_template('student/add.html',
                               **colorThemes['default'])
