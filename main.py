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

        if not title_name or not body_name:
            return render_template('newpost.html',title_error="The title is empty.", body_error = "The body is empty.")            

        newpost = Blog(title_name, body_name)
        db.session.add(newpost)
        db.session.commit()

        return redirect("/blog")

    return render_template('newpost.html',title="Build a Blog")


@app.route('/blog', methods=['GET'])
def blog():
 
    id = request.args.get("id")

    if id:  

        print("In Id................... id.....")

        blog_var =  Blog.query.filter_by(id=id).first()
        #blog_var = Blog.query.get(id=id)

        print("The id we got from the database is ", blog_var)

        return render_template('blog_post.html',title="Build a Blog", blog_var = blog_var)

    else:

        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)



if __name__ == '__main__':
    app.run()