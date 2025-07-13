from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "deadline": self.deadline
        }

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    # ✅ Ensure the database table is created at runtime
    with app.app_context():
        db.create_all()

    if request.method == 'POST':
        task_name = request.form['task']
        task_deadline = request.form['deadline']
        new_task = Task(name=task_name, deadline=task_deadline)

        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            db.session.rollback()

    tasks = Task.query.all()
    tasks_dict = [task.to_dict() for task in tasks]
    today = datetime.today().strftime('%Y-%m-%d')

    return render_template('index.html', tasks=tasks_dict, today=today)

# Delete route
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task."

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
