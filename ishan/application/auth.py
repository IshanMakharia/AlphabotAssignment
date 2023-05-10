from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from application.models import *
from application.database import db


auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template('index.html', name = current_user.username if current_user.is_authenticated else "Login to use application...")

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    ph = request.form.get('ph')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(id=ph).first()

    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('auth.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    ph = request.form.get('ph')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(id=ph).first()

    if user:
        flash('Mobile number already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(id=ph, username=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))




@auth.route('/notes/getAll')
@login_required
def get_all_notes():
    notes = Note.query.filter_by(user_id=current_user.id)
    note_list = []
    for note in notes:
        note_list.append({"id":note.id, "title": note.title, "content": note.content})
    return render_template('getNote.html', notes=note_list)


@auth.route('/notes/add')
@login_required
def add_note():
    return render_template('addNote.html')

@auth.route('/notes/add', methods=['POST'])
@login_required
def add_note_post():
    title = request.form.get('title')
    content = request.form.get('content')
    id = Note.query.count()+1
    query=Note(id=id,title=title,content=content,user_id=current_user.id)
    db.session.add(query)
    db.session.commit()
    return render_template('result.html')



@auth.route('/notes/get/<int:id>')
@login_required
def get_notes(id):
    note = Note.query.filter_by(id=id).first()
    return render_template('editNote.html', note={"id":note.id,"title":note.title,"content":note.content})




@auth.route('/notes/delete/<int:id>', methods=['GET', 'DELETE'])
@login_required
def delete_notes(id):
    page=Note.query.filter_by(id=id).first()
    if page is None:
        return "enter valid id"
    else:
        db.session.delete(page)
        db.session.commit()
        return render_template('result.html')


@auth.route('/notes/update/<int:id>', methods=['POST', 'PUT'])
@login_required
def update_notes_post(id):
    page=Note.query.filter_by(id=id).first()
    if page is None:
        return "enter valid id"
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        page.title,page.content=title,content
        db.session.commit()
        return render_template('result.html')
  