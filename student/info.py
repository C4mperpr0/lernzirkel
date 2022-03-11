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

studentInfo = Blueprint("list", __name__, static_folder="static", template_folder="templates/student")


@studentInfo.route('/<string:studentname>', methods=['GET', 'POST'])
def studentList_():
    print(studentname)
    return render_template('info.html',
                           **colorThemes['default'])
