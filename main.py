
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:xxx@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #completed = db.Column(db.Boolean)

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        #self.completed = False
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','index','blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
   

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST':
        post_title = request.form['posttitle']
        post_body = request.form['postbody']
        new_post = Blog(post_title,post_body,owner)
        post_title_error=''
        post_body_error=''
        if len(post_title) <1:
            flash('Please try again', 'error')
            post_title_error="enter title "
            return render_template('newpost.html')
        
        if len(post_body)<1:
            post_body_error="enter body"
            flash('Please try again', 'error')
            return render_template('newpost.html')

        if not post_title_error and not post_body_error:
            db.session.add(new_post)
            db.session.commit()
            return render_template('newpost.html')
        else:
            return render_template('newpost.html',post_title_error=post_title_error,post_body_error=post_body_error)
    else:
        return render_template('newpost.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    userposts = User.query.all()
    return render_template('index.html',title="Users!", 
        userposts=userposts)
    
    #xxxcutxxx



@app.route('/blog', methods=['POST', 'GET'])
def blog():
    
    blogpost = Blog.query.all()
    
    
    
    #userId = Blog.query.get('id') 
    userId = request.args.get('user')
        
    
    
    #owner = User.query.filter_by(blogs=request.args.get('user')).all()
    
    #owner = User.query.filter_by(blogs=userId).first()
    if 'id' in request.args:
        #user = User.query.get(userId) 
        postid = request.args.get('id')
        post = Blog.query.get(postid)  
        return render_template('blogpage.html',title="Post Page",blogpost=blogpost,post=post)

    if 'user' in request.args: 
        user = User.query.get(userId) 
        viewpost = Blog.query.get(userId) 
        blogs=Blog.query.filter_by(owner=user).all() 
        return render_template('singleUser.html',title="User Page",blogpost=blogpost,viewpost=viewpost,user=user,blogs=blogs)
    else:
        
        #completed_tasks = Task.query.filter_by(completed=True).all()
        #postid = request.args.get('id')
        #user = Blog.query.get(postid) 
        return render_template('blog.html',title="Blog!", 
        blogpost=blogpost)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify']

        username_error=''
        password_error=''
        verify_password_error=''
        email_error=''
        
        # TODO - validate user's data
        if ' ' in username:
            username_error='Not a valid username'
        
        else:
            if len(username) <3 or len(username)>20:
                username_error='Enter a username between 3 and 20 characters long'
            
   
        if ' ' in password:
            password_error='Not a valid password'
            password=''

        if len(password) <3 or len(password)>20:
            password_error='Enter a password between 3 and 20 characters long'
            password=''

        if verify_password != password:
            verify_password_error='passwords do not match'
            verify_password=''
    
    
        if  username_error and not password_error and not verify_password_error:
            return render_template('signup.html',username_error=username_error, password_error=password_error, verify_password_error=verify_password_error, username=username,password=password, verify_password=verify_password)


        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"
    
        #return redirect('/newpost?username={0}'.format(username))
    return render_template('signup.html',title="signup!")

        

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()
