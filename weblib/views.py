import json

from flask import render_template, flash, redirect, session, url_for, request

from . import app
from .database import db_session
from .forms import LoginForm, RegistrationForm, BookForm, AuthorForm, SearchForm
from .models import Book, Author, User


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session.query(User).filter_by(username=form.username.data).first()
        if not user:
            return json.dumps({'message': 'Неверный логин или пароль!'})
        elif not user.check_password(form.password.data):
            return json.dumps({'message': 'Неверный логин или пароль!'})
        else:
            session['logged_in'] = True
            return json.dumps({'message': 'Вы удачно вошли!', 'success': True})

        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password_one.data)
        db_session.add(user)
        try:
            db_session.commit()
            session['logged_in'] = True
            return json.dumps({'message': 'Успешная регистрация.',
                               'success': True})
        except:
            return json.dumps({'message': 'Пользователь с таким именем уже есть.',
                               'success': False})
    return render_template('registration.html', form=form)


@app.route('/books')
def books():
    return render_template('books.html', books=db_session.query(Book).all())


@app.route('/authors')
def authors():
    return render_template('authors.html', authors=db_session.query(Author).all())


@app.route('/book/<book_id>', methods=['GET', 'POST'])
def book(book_id):
    book = db_session.query(Book).get(book_id)
    authors = db_session.query(Author).all()
    if book is None:
        flash('К сожалению, данной книги уже нет в нашей базе.')
        return redirect(url_for('index'))

    form = BookForm(title=book.title, abstract=book.abstract)

    if form.validate_on_submit():
        if not session['logged_in']:
            flash('У вас нет прав на редактирование книги.')
            return redirect(url_for('index'))

        ids = request.form.getlist('authors')
        if ids:
            book.authors = db_session.query(Author).filter(Author.id.in_(ids)).all()

        book.title = form.title.data
        book.abstract = form.abstract.data
        db_session.add(book)
        db_session.commit()
        return json.dumps({'message': 'Изменения сохранены.', 'success': True})

    return render_template('book.html', book=book, form=form, authors=authors)


@app.route('/author/<author_id>', methods=['GET', 'POST'])
def author(author_id):
    author = db_session.query(Author).get(author_id)
    books = db_session.query(Book).all()

    form = AuthorForm(name=author.name, biography=author.biography)

    if form.validate_on_submit():
        if not session['logged_in']:
            flash('У вас нет прав на редактирование автора.')
            return redirect(url_for('index'))

        ids = request.form.getlist('books')
        if ids:
            author.books = db_session.query(Book).filter(Book.id.in_(ids)).all()

        author.name = form.name.data
        db_session.add(author)
        db_session.commit()
        return json.dumps({'message': 'Изменения сохранены.', 'success': True})

    return render_template('author.html', author=author,
                           form=form, books=books)


@app.route('/del/book/<book_id>')
def del_book(book_id):
    if not session['logged_in']:
        flash('У вас нет прав на удаление книги.')
        return redirect(url_for('index'))

    book = db_session.query(Book).get(book_id)
    db_session.delete(book)
    db_session.commit()
    return redirect(url_for('books'))


@app.route('/del/author/<author_id>')
def del_author(author_id):
    if not session['logged_in']:
        flash('У вас нет прав на удаление автора.')
        return redirect(url_for('index'))

    author = db_session.query(Author).get(author_id)
    db_session.delete(author)
    db_session.commit()
    return redirect(url_for('authors'))


@app.route('/new/book/', methods=['GET', 'POST'])
def new_book():
    if not session['logged_in']:
        flash('У вас нет прав на добавление книги.')
        return redirect(url_for('index'))

    form = BookForm()
    authors = db_session.query(Author).all()

    if form.validate_on_submit():
        book = Book(
            form.title.data,
            form.abstract.data,
        )

        ids = request.form.getlist('authors')
        book.authors = db_session.query(Author).filter(Author.id.in_(ids)).all()

        db_session.add(book)
        db_session.commit()

        return redirect(url_for('books'))
    return render_template('new_book.html', form=form, authors=authors)


@app.route('/new/author/', methods=['GET', 'POST'])
def new_author():
    if not session['logged_in']:
        flash('У вас нет прав на добавление автора.')
        return redirect(url_for('index'))

    form = AuthorForm()
    books = db_session.query(Book).all()

    if form.validate_on_submit():
        author = Author(
            form.name.data,
        )

        ids = request.form.getlist('books')
        author.books = db_session.query(Book).filter(Book.id.in_(ids)).all()

        db_session.add(author)
        db_session.commit()

        return redirect(url_for('authors'))
    return render_template('new_author.html', form=form, books=books)


@app.route('/search', methods=['GET', 'POST'])
def search(exception=None):
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        query = '%{}%'.format(query)
        books = db_session.query(Book).filter(Book.title.ilike(query)).all()
        author = db_session.query(Author).filter(Author.name.ilike(query)).first()
        if author:
            books = db_session.query(Book).filter(Book.authors.any(Author.id == author.id))

        if not books:
            fail = True
            return render_template('search.html', form=form, fail=fail)

        return render_template('search.html', form=form, books=books)

    return render_template('search.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
