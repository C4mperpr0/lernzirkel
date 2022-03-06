from flask import *
from flask import make_response
import os

docs = Blueprint("docs", __name__)


@docs.route('/')
def docs_():
    print(os.listdir())
    with open("docs/lernzirkel.pdf", "rb") as file:
        binary_pdf = file.read()
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=lernzirkel.pdf'
    return response
