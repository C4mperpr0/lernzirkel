from flask import *
import json
import time

from serverconfig import Serverconfig

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

login = Blueprint("login", __name__, static_folder="static", template_folder="templates")


@login.route('/', methods=['GET', 'POST'])
def login_():
    if request.method == 'GET':
        if 'user_id' in session.keys():
            return f"moin {escape(session['teacher_id'])}"
        return render_template('teacher/login.html',
                               redirect_url=url_for('dashboard.dashboard_'),
                               **colorThemes['default'])
    else:
        time.sleep(1)
        teacher_object = current_app.DbClasses.Teacher.query.filter(current_app.DbClasses.Teacher.id == request.form['teacher_id']).one()
        if teacher_object.check_login(request.form['password']) and teacher_object.verified:
            session['teacher_id'] = teacher_object.id
            session['teacher_forename'] = teacher_object.forename
            session['teacher_surname'] = teacher_object.surname
            session['teacher_subjects'] = teacher_object.subjects
            session['teacher_admin'] = teacher_object.admin
            print(f"Teacher with id {request.form['teacher_id']} successfully loged in!")
            return jsonify({'login': True})
        else:
            return jsonify({'error': 'loginerror'})
