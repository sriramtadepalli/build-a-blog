from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))


    def __init__(self, title, body): # Blog()
        self.title = title
        self.body = body



@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        newpost = Blog(title_name, body_name)
        db.session.add(newpost)
        db.session.commit()

        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)

    return render_template('newpost.html',title="Build a Blog")


@app.route('/blog', methods=['POST'])
def blog():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)

    db.session.add(task)
    db.session.commit()

    return redirect('/newpost')


if __name__ == '__main__':
    app.run()