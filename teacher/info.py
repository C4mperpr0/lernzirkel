import requests
from flask import *
import json
from sqlalchemy import asc, desc
from werkzeug.utils import secure_filename

from serverconfig import Serverconfig
Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

teacherInfo = Blueprint("teacherInfo", __name__, static_folder="static", template_folder="templates")


@teacherInfo.route('/<int:teacherid>', methods=['GET', 'POST'])
def teacherInfo_(teacherid):
    print(teacherid)
    data = current_app.DbClasses.Teacher.query.filter(current_app.DbClasses.Teacher.id == teacherid).one_or_none()
    print(data)
    return f"<h1>Da number is {teacherid} for {data}</h1>"

"""
    return render_template('teacher/info.html',
                           **colorThemes['default'])
"""
