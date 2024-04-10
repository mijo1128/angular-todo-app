from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True
cors = CORS()
cors.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
app.app_context().push()

taskFields = {
    'id': fields.Integer,
    'text': fields.String,
    'day': fields.String,
    'reminder': fields.Boolean

}


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    day = db.Column(db.String, nullable=False)
    reminder= db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return self.text

class Items(Resource):
    @marshal_with(taskFields)
    def get(self):
        tasks = Task.query.all()
        return tasks
    
    @marshal_with(taskFields)
    def post(self):
        data = request.json
        task = Task(text=data['text'],day=data['day'])
        db.session.add(task)
        db.session.commit()
        tasks = Task.query.all()
        # taskId = len(fakeDatabase.keys()) + 1
        # fakeDatabase[taskId] = {'task': data['task']}
        return tasks

class Item(Resource):

    @marshal_with(taskFields)
    def get(self, pk):
        task = Task.query.filter_by(id=pk).first()
        return task
    

    @marshal_with(taskFields)
    def put(self, pk):
        data = request.json
        task = Task.query.filter_by(id=pk).first()
        task.text = data['text']
        task.day = data['day']
        task.reminder = data['reminder']
        db.session.commit()
        return task

    @marshal_with(taskFields)
    def delete(self, pk):
        task = Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        tasks = Task.query.all()
        return tasks

    
api.add_resource(Items,'/')
api.add_resource(Item,'/<int:pk>')


if __name__ == "__main__":
    app.run()