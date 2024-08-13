from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from forms import NewPost
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from flask_ckeditor.utils import cleanify
from datetime import date



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # Query the database for all the posts. Convert the data to a python list.
    get_all = db.session.execute(db.select(BlogPost).order_by(BlogPost.date)).scalars().all()
    posts = [post for post in get_all]
    return render_template("index.html", all_posts=posts)


# Add a route so that you can click on individual posts.
@app.route('/<int:post_id>')
def show_post(post_id):
    # Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.execute(db.select(BlogPost).filter_by(id=post_id)).scalar()
    return render_template("post.html", post=requested_post)


# Create a new blog post
@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = NewPost()

    if request.method == "POST":
        # data = cleanify(request.form.get('ckeditor'))
        if form.validate_on_submit():
            title = form.title.data.title()
            subtitle = form.subtitle.data
            body = form.body.data
            author = form.author.data.title()
            img_url = form.img_url.data

            post_date = date.today().strftime('%B %d, %Y')

            new_post = BlogPost(title=title, subtitle=subtitle, body=body, author=author, img_url=img_url, date=post_date)

            with app.app_context():
                db.session.add(new_post)
                db.session.commit()

            return redirect("/")

    return render_template("make-post.html", form=form)

# TODO: edit_post() to change an existing blog post

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
