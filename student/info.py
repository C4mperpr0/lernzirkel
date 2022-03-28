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

studentInfo = Blueprint("info", __name__, static_folder="static", template_folder="templates/student")


@studentInfo.route('/<int:studentid>', methods=['GET', 'POST'])
def studentInfo_(studentid):
    print(studentid)
    data = current_app.DbClasses.Student.query.filter(current_app.DbClasses.Student.id == studentid).one_or_none()
    print(data)
    return f"<h1>Da number is {studentid} for {data}</h1>"

"""
    return render_template('info.html',
                           **colorThemes['default'])
"""
