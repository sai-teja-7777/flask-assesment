from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    company_name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(30), nullable = False)
    phone_number = db.Column(db.Integer, nullable = False )
    address =  db.Column(db.String(300), nullable = False)
    ceo_name = db.Column(db.String(30))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return self.company_name

 
@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        CN = request.form['company_name']
        E = request.form['email']
        PN = request.form['phone_number']
        A = request.form['address']
        CN = request.form['ceo_name']
        new_task = Todo(company_name = CN , email = E, phone_number = PN , address = A , ceo_name = CN)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting this task"

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':

        task.company_name= request.form['company_name']
        task.email = request.form['email']
        task.phone_number = request.form['phone_number']
        task.address = request.form['address']
        task.ceo_name = request.form['ceo_name']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating this task"
    else:
        return render_template('update.html',task = task)
@app.route('/search', methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        data = Todo.query.filter_by(phone_number=request.form['phone_number']).all()
        if len(data) !=0:
            return render_template('index.html',tasks = data)
        else:
            return "<center><h4>There is no company with given Phone number. Please check the phone number and try again!</h4></center>"
    else:
        return redirect('/')

        
            
        
if __name__ == "__main__":
    app.run(debug=True)
