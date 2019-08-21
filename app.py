from flask import Flask, g, render_template, redirect, flash, url_for
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, current_user, logout_user,
                            login_required)
from slugify import slugify

import forms
import models
import datetime

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'sdlhery734t4fVG$#TI4ugf48hof'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
@app.route('/entries/')
def index():
    journals = models.Journal.select()
    return render_template('index.html', journals = journals)

@app.route('/entries/tag/<tag>')
def show_tag(tag):
    journals = models.Journal.select().where(models.Journal.tag == tag)
    return render_template('index.html', journals = journals)

@app.route('/entries/new', methods=('GET', 'POST'))
def new():
    form = forms.JournalForm()
    if form.validate_on_submit():
        #flash(" Submit success!! ")
        try:
            models.Journal.create_journal(
                title = form.title.data,
                date = form.date.data,
                time_spent = form.time_spent.data,
                what_you_lean = form.what_you_lean.data,
                resource_to_remember = form.resource_to_remember.data,
                tag = form.tag.data
            )
        except ValueError:
            flash('Title already exists')
            return render_template('new.html', form = form)
        models.Tag.create(
            tag_on_journal = models.Journal.get(
                models.Journal.title == form.title.data),
            tag_name = form.tag.data
        )
        return redirect(url_for('index'))
    return render_template('new.html', form = form)


@app.route('/entries/<slug>')
def detail(slug):
    journal = models.Journal.get(models.Journal.slug == slug)
    return render_template('detail.html', journal = journal)

@app.route('/entries/<slug>/edit', methods=('GET', 'POST'))
def edit(slug):
    form = forms.JournalForm()
    journal = models.Journal.get(models.Journal.slug == slug)
    tag = models.Tag.get(
            models.Tag.tag_on_journal == journal,
            models.Tag.tag_name == journal.tag)
    if form.validate_on_submit():
        # from update query http://docs.peewee-orm.com/en/latest/peewee/api.html#Model.update
        journal.title = form.title.data
        journal.date = form.date.data
        journal.time_spent = form.time_spent.data
        journal.what_you_lean = form.what_you_lean.data
        journal.resource_to_remember = form.resource_to_remember.data
        if journal.tag != form.tag.data:
            tag.tag_name = form.tag.data
            journal.tag = form.tag.data

        journal.slug = slugify(form.title.data)
        try:
            tag.save()
            journal.save()
        except models.IntegrityError:
            flash('Title already exists')
            return render_template('edit.html', form=form , journal=journal)
        # from end
        return redirect(url_for('detail', slug=slugify(form.title.data)))
    return render_template('edit.html', form=form , journal=journal)

@app.route('/entries/<slug>/delete')
def delete(slug):
    journal = models.Journal.get(models.Journal.slug == slug)
    try:
        models.Tag.get(
            models.Tag.tag_on_journal == journal,
            models.Tag.tag_name == journal.tag
            ).delete_instance()
        journal.delete_instance()
    except models.IntegrityError:
        flash("IntegrityError")

    return redirect(url_for('index'))


@app.route('/register',  methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        try:
            models.User.create_user(username = form.username.data,
                password=form.password.data)
        except models.IntegrityError:
            flash("Existing User! Please use another name")
            return render_template('register.html', form=form)
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login',  methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username==form.username.data)
        except models.DoesNotExist:
            flash('User is not exist!!')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("you are login!!")
                return redirect(url_for('index'))
            else:
                flash("Pasword is not correct!!")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!")
    return redirect(url_for('index'))

def create_journal_user():
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
    try:
        models.User.create_user(
            username = "frank",
            password = "password"
        )
    except ValueError:
        pass



if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
