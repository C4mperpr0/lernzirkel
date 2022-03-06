from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lernzirkel.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)

    class Student(db.Model):
        id = db.Column(db.Integer(), primary_key=True, nullable=False)
        forename = db.Column(db.String(), nullable=False)
        surname = db.Column(db.String(), nullable=False)
        grade = db.Column(db.String(), nullable=False)
        school = db.Column(db.String(), nullable=False)
        subjects = db.Column(db.String(), default=None)
        mail = db.Column(db.String(), default=None)
        phone = db.Column(db.String(), default=None)
        student_creation = db.Column(db.DateTime, default=datetime.now())

        def as_dict(self):
            data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
            data['student_creation'] = data['student_creation'].strftime("%d.%m.%Y %H:%M")
            return data

        def __repr__(self):
            return f"{(self.forename + ' ' + self.surname).replace(' ', '_')}#{self.id}"

    class Timetable(db.Model):
        id = db.Column(db.Integer(), primary_key=True, nullable=False)
        student = db.Column(db.String(), nullable=False)
        teacher = db.Column(db.String(), nullable=False)
        date = db.Column(db.DateTime, nullable=False)
        status = db.Column(db.String(), nullable=False, default="pending")
        subject = db.Column(db.String(), nullable=True, default=None)
        comment = db.Column(db.String(), nullable=False, default="")
        regular_id = db.Column(db.Integer(), nullable=True, default=None)

        def as_dict(self, date_as_string=False):
            data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
            if date_as_string:
                data['date'] = data['date'].strftime("%d-%m-%Y")
            return data

    class TimetableRegular(db.Model):
        id = db.Column(db.Integer(), primary_key=True, nullable=False)
        student = db.Column(db.String(), nullable=False)
        teacher = db.Column(db.String(), nullable=False)
        day = db.Column(db.Integer(), nullable=False) # days as 0 to 6 (0 is sunday)
        subject = db.Column(db.String(), nullable=True)

    db.create_all()
    app.db = db

    class DbClasses:
        def __init__(self):
            self.Student = Student
            self.Timetable = Timetable
            self.TimetableRegular = TimetableRegular

    app.DbClasses = DbClasses()
