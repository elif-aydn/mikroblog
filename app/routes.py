from datetime import datetime, timezone

from flask_wtf import form
from app import app, db  # app paketinin içindeki app adlı Flask nesnesini getir.
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

import sqlalchemy as sa
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User

from urllib.parse import urlsplit

from flask import flash, redirect, render_template, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.forms import EmptyForm
from app.forms import PostForm
from app.models import Post

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
# Bunlar birer dekoratördür. URL adresleriyle Python fonksiyonunu eşleştirirler.
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))

    user = {
        'username': 'Elif'
    }
    # Burada geçici bir kullanıcı oluşturduk.
    # Gerçek sistem henüz hazır değilken kullanılan bu tür verilere
    # mock data, yani sahte/örnek veri denir.

    # posts, iki sözlük içeren bir listedir.
    posts = db.session.scalars(current_user.following_posts()).all()
    
    return render_template(
        'index.html',        # İşlenecek şablon dosyası
        title='Ana Sayfa',   # HTML'e gönderilen başlık
        user=user,           # HTML'e gönderilen kullanıcı sözlüğü
                             # Soldaki user: Jinja değişkeni
                             # Sağdaki user: Python değişkeni
        posts=posts,         # HTML'e gönderilen gönderiler listesi
        form=form            # HTML'e gönderilen form nesnesi
    )


# Bu bir görünüm fonksiyonudur.
# Fonksiyon, index.html şablonunu işleyerek tarayıcıya gönderilecek HTTP yanıtını oluşturur.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(
                User.username == form.username.data
            )
        )

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    next_page = request.args.get('next')

    if not next_page or urlsplit(next_page).netloc != '':
        next_page = url_for('index')

    return redirect(next_page)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template(
        'register.html',
        title='Register',
        form=form
    )

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(
        sa.select(User).where(User.username == username)
    )
    form = EmptyForm()
    return render_template("user.html", user=user, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(
    original_username=current_user.username
)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data

        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template(
        'edit_profile.html',
        title='Edit Profile',
        form=form
    )

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.session.scalars(query).all()
    return render_template('index.html', title='Explore', posts=posts)

# @app.route("/senol")
# def senol():
#     deneme=[
#         1,2,3,4,5,6,7,8,9,10
#     ]
#     return render_template("senol.html", deneme=deneme)