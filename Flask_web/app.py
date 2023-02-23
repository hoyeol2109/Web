from flask import Flask, render_template, request, redirect, url_for
import os
from models import db
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
with app.app_context():
    db.create_all()

# store reviews in a list
reviews = []

@app.route('/')
def index():
    # render the review form
    return render_template('review_form.html')

@app.route('/submit_review', methods=['POST'])
def submit_review():
    # get the form data
    title = request.form['title']
    author = request.form['author']
    review = request.form['review']

    # add the review to the list
    reviews.append({'title': title, 'author': author, 'review': review})

    # redirect to the review list page
    return redirect(url_for('review_list'))

@app.route('/reviews')
def review_list():
    # render the review list template with the reviews data
    return render_template('review_list.html', reviews=reviews)


@app.route('/topic')
def topic():
    return render_template('topic.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        topic = request.form['topic']
        return render_template('post.html', topic=topic)
    return render_template('post.html')

@app.route('/reply', methods=['GET', 'POST'])
def reply():
    if request.method == 'POST':
        answer = request.form['answer']
        return render_template('reply.html', answer=answer)
    return render_template('reply.html')


if __name__ == '__main__':
    app.run()#host = "0.0.0.0", port=5000)