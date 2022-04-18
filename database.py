from datetime import datetime, timedelta
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

        def as_dict(self, date_as_string=False, date_as_json=False):
            data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
            if date_as_string:
                data['date'] = data['date'].strftime("%d-%m-%Y")
            elif date_as_json:
                data['date'] = {"year": data['date'].year, "month": data['date'].month, "day": data['date'].day}
            return data

    class TimetableRegular(db.Model):
        id = db.Column(db.Integer(), primary_key=True, nullable=False)
        student = db.Column(db.String(), nullable=False)
        teacher = db.Column(db.String(), nullable=False)
        day = db.Column(db.Integer(), nullable=False) # days as 0 to 6 (0 is monday)
        subject = db.Column(db.String(), nullable=True)

        def as_timetable(self, year, month, date_as_json=False):
            dates = []
            offset = self.day - datetime(year, month, 1).weekday()
            print(f"offset: {offset}")
            for i in range(6):
                t = datetime(year, month, 1) + timedelta(days=offset+(7*i))
                print(t)
                if t.month == month:
                    dates.append(t)
            
            data = []
            for d in dates:
                data.append({"student": self.student,
                            "teacher": self.teacher,
                            "date": {"year": d.year, "month": d.month, "day": d.day} if date_as_json else d,
                            "status": "pending",
                            "subject": self.subject,
                            "comment": "",
                            "regular_id": self.id})
            return data

    db.create_all()
    app.db = db

    class DbClasses:
        def __init__(self):
            self.Student = Student
            self.Timetable = Timetable
            self.TimetableRegular = TimetableRegular

    app.DbClasses = DbClasses()
