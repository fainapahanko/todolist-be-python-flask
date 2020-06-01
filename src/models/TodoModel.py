from marshmallow import fields, Schema
from datetime import datetime
from . import db


class TodoModel(db.Model):

    # table name
    __tablename__ = 'to_dos'

    id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(50), nullable=False)
    task_content = db.Column(db.String(400), nullable=False)
    completed = db.Column(db.Integer, default=0)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime)

    def __init__(self, data):
        self.task_title = data.get('task_title')
        self.task_content = data.get('task_content')
        self.user = data.get('user_id')
        self.date_updated = datetime.utcnow()
        self.date_created = datetime.utcnow()


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.date_updated = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_task():
        return TodoModel.query.all()

    @staticmethod
    def get_one_task(id):
        return TodoModel.query.get(id)

    @staticmethod
    def get_all_task_for_user(user_id):
        return TodoModel.query.filter_by(user=user_id).all()

    def __repr__(self):
        return '<Task %r>' % self.id


class TodoSchema(Schema):
    """
    TodoModel Schema
    """
    id = fields.Int(dump_only=True)
    task_title = fields.Str(required=True)
    task_content = fields.Str(required=True)
    completed = fields.Int(required=True)
    user = fields.Int(required=True)
    date_created = fields.DateTime(dump_only=True)
    date_updated = fields.DateTime(dump_only=True)
