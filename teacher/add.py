from flask import *
import json
import time
from sqlalchemy import desc
import hashlib

from serverconfig import Serverconfig


Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

teacherAdd = Blueprint("teacherAdd", __name__, static_folder="static", template_folder="templates")


@teacherAdd.route('/', methods=['GET', 'POST'])
def teacherAdd_():
    if request.method == 'POST':
        time.sleep(1)
        print(request.form)

        # check for errors
        
        teacher_id = current_app.DbClasses.Teacher.query.order_by(desc(current_app.DbClasses.Teacher.id)).first()
        current_app.db.session.add(current_app.DbClasses.Teacher(id=1+int(teacher_id.id) if teacher_id is not None else 0,
                                                                 forename=request.form["forename"],
                                                                 surname=request.form["surname"],
                                                                 admin=1 if teacher_id is None else 0,
                                                                 verified=1 if teacher_id is None else 0,
                                                                 password=hashlib.sha512(request.form["password"].encode("utf8")).hexdigest(),
                                                                 subjects=request.form["subjects"],
                                                                 mail=request.form["mail"].lower(),
                                                                 phone=request.form["phone"]))
        current_app.db.session.commit()

        return jsonify({'visiturl': '/student/list'})

    else:
        return render_template('teacher/add.html',
                               **colorThemes['default'])
