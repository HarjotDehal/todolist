from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)
# THIS JUST references this file

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'
# this is a siomple sql database to use. three / is relative path. 4 is absolute. reside in project location. everything in test.db

db = SQLAlchemy(app)

class Todo(db.Model):
    # we have our class so set up ids of entries and stuff
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
# cant leave task empty
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime, default =datetime.utcnow)

    # anytime a new entry it creaetd, date of that time is set
    # when we ask for something, it will return the id of the task
    def __repr(self):
        return '<Task %r>' %self.id



# set up our databse with following in command line

# python
# from app import db
# db.create_all()

# exit()
# this sets up our databsse. 

# setup routes with decorator. our home page


@app.route('/',methods=['POST','GET'])
# 2 methods which it can accept
# make this for our homepage

def index():

    if request.method == "POST":
    # basically create a new page here when setting it up
        task_content=request.form['content']
        newTask = Todo(content = task_content)
        # gets our to do model, now push it to our database
        
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding the task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        # gets all the current tasks and pass it to template
        return render_template('index.html',tasks=tasks)

    
# this is for our html it seems

# template inheritance. create onoe master html and then you can create sub page and just insert code where you need it. 
# index html is our main skeleton page


# create route for deleting
# need unique element which is key id cuz task can be same
@app.route('/delete/<int:id>')

def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    # if it doesnt get id then 404
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'A error occurred deleting the task'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    # query for the task we need with our id. 
    if request.method=='POST':
        # update our task when we update
        task.content = request.form['content']
        try: 
            db.session.commit()
            return redirect('/')
        # return back to our home page
        except:
            return 'There was an error updating'
    else: 
        # pass task to this
        return render_template('update.html',task=task)

if __name__ == "__main__":
    app.run(debug=True)