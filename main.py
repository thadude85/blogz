
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:xxx@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    #completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        #self.completed = False


#@app.route('/', methods=['POST', 'GET'])
#def index():


   

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        post_title = request.form['posttitle']
        post_body = request.form['postbody']
        new_post = Blog(post_title,post_body)
        post_title_error=''
        post_body_error=''
        if post_title.isspace():
            post_title_error="enter title"
        if post_body.isspace():
            post_body_error="enter body"
        if not post_title_error and not post_body_error:
            db.session.add(new_post)
            db.session.commit()
            return render_template('newpost.html')
        else:
            return render_template('newpost.html',post_title_error=post_title_error,post_body_error=post_body_error)
        
        
    else:
        return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    
    blogpost = Blog.query.all()
    if 'id' in request.args:
        postid = request.args.get('id')
        viewpost = Blog.query.get(postid)   
        return render_template('blogpage.html',title="Post Page",blogpost=blogpost,viewpost=viewpost)

    else:
        #completed_tasks = Task.query.filter_by(completed=True).all()
        return render_template('blog.html',title="Blog!", 
        blogpost=blogpost)



if __name__ == '__main__':
    app.run()
