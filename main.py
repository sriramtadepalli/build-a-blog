from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "blogz"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, body): 
        self.title = title
        self.body = body
        self.owner = owner 

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(200))
    blogs = db.relationship('Blog', backref='owner')
    #blogs


    def __init__(self, username, password): 
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods = ['POST', 'GET'] )
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=session['username']).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            #return redirect('/newpost')
            # return render_template('login.html')

        else:
            flash('User password incorrect, or user does not exist', 'error')

    if request.method == 'GET':
        pass
        # return render_template('login.html')

    
    return render_template('/login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if not username or len(username) > 3 or len(username) > 20:
            flash("error:Invalid username")
            # flash("Invalid username", "error")

        elif not password or len(password) > 3 or len(password) > 20:
            flash("Invalid password", "error")


        elif password != verify:
            flash("Not a valid password", "error")

        else:
            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                flash("User already exists", "error")
            
            else:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/newpost')

@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        owner = User.query.filter_by(username=session['username']).first() # Get owner from your session instead of owner field that doesen't exist.

        

        if not title_name or not body_name:
            return render_template('newpost.html',title_error="The title is empty.", body_error = "The body is empty.")            

        newpost = Blog(title_name, body_name, owner_id_name)
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