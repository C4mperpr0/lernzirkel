from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lernzirkel.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)

    class Student(db.Model):
        id = db.Column(db.Integer(), primary_key=True, nullable=False)
        forename = db.Column(db.String(1), nullable=False)
        surname = db.Column(db.String(1), nullable=False)
        grade = db.Column(db.String(0), nullable=False)
        school = db.Column(db.String(0), nullable=False)
        subjects = db.Column(db.String(0), default=None)
        mail = db.Column(db.String(1), default=None)
        phone = db.Column(db.String(0), default=None)
        student_creation = db.Column(db.DateTime, default=datetime.now())

        def as_dict(self):
            data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
            data['student_creation'] = data['student_creation'].strftime("%d.%m.%Y %H:%M")
            return data

        def __repr__(self):
            return f"{(self.forename + ' ' + self.surname).replace(' ', '_')}#{self.id}"

    db.create_all()
    app.db = db

    class DbClasses:
        def __init__(self):
            self.Student = Student

    app.DbClasses = DbClasses()
