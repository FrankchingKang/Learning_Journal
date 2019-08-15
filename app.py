from flask import Flask, g, render_template, redirect, flash, url_for
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user

import forms
import models
import datetime

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'sdlhery734t4fVG$#TI4ugf48hof'


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
def index():
    journals = models.Journal.select()
    return render_template('index.html', journals = journals)

@app.route('/entries/<tag>')
def show_tag(tag):
    journals = models.Journal.select().where(models.Journal.tag == tag)
    return render_template('index.html', journals = journals)

@app.route('/entries/new', methods=('GET', 'POST'))
def new():
    form = forms.JournalForm()
    if form.validate_on_submit():
        flash(" submit success!! ")
        models.Journal.create_journal(
            title = form.title.data,
            date = form.date.data,
            time_spent = form.time_spent.data,
            what_you_lean = form.what_you_lean.data,
            resource_to_remember = form.resource_to_remember.data,
            tag = form.tag.data
        )
        return redirect(url_for('index'))

    return render_template('new.html', form = form)


@app.route('/entries/<int:id>')
def detail(id):
    journal = models.Journal.get(models.Journal.id == id)
    return render_template('detail.html', journal = journal)

@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    form = forms.JournalForm()
    journal = models.Journal.get(models.Journal.id == id)
    if form.validate_on_submit():
        # from update query http://docs.peewee-orm.com/en/latest/peewee/api.html#Model.update
        q = models.Journal.update(
            title = form.title.data,
            date = form.date.data,
            time_spent = form.time_spent.data,
            resource_to_remember = form.resource_to_remember.data,
            tag = form.tag.data
        ).where(models.Journal.id == id)
        q.execute()
        # from end
        return redirect(url_for('detail', id=journal.id))

    return render_template('edit.html', form=form , journal=journal)

@app.route('/entries/<int:id>/delete')
def delete(id):
    try:
        models.Journal.get(models.Journal.id == id).delete_instance()
    except models.IntegrityError:
        flash("IntegrityError")

    return redirect(url_for('index'))


@app.route('/register',  methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("singup successfully")
        models.User.create_user(username = form.username.data,
            password=form.password.data)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login',  methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(username==form.username.data)
        except models.DoesNotExist:
            flash('User is not exist!!')
        if check_password_hash(password, form.password.data):
            login_user(user)
            flash("you are login!!")
            return redirect(url_for('index'))
        else:
            flash("Pasword is not correct!!")
    return render_template('login.html', form=form)


if __name__ == '__main__':
    models.initialize()
    try:
        models.Journal.create_journal(
                title = 'python flask journal web',
                date = datetime.date.today(),
                time_spent = 2,
                what_you_lean = "web side flask",
                resource_to_remember = "treehouse",
                tag = "test")

    except ValueError:
        pass

    app.run(debug=DEBUG, host=HOST, port=PORT)
