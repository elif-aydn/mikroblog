from app import app, db  # app paketinin içindeki app adlı Flask nesnesini getir.
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

import sqlalchemy as sa
from flask_login import current_user, login_user, logout_user
from app.models import User

@app.route('/')
@app.route('/index')
# Bunlar birer dekoratördür. URL adresleriyle Python fonksiyonunu eşleştirirler.
def index():
    user = {
        'username': 'Elif'
    }
    # Burada geçici bir kullanıcı oluşturduk.
    # Gerçek sistem henüz hazır değilken kullanılan bu tür verilere
    # mock data, yani sahte/örnek veri denir.

    # posts, iki sözlük içeren bir listedir.
    posts = [
        {
            'author': {'username': 'Mehmet'},
            'body': 'Bugün Flask şablonlarını öğreniyorum.'
        },
        {
            'author': {'username': 'Ayşe'},
            'body': 'Jinja ile dinamik HTML oluşturmak oldukça kullanışlı.'
        }
    ]

    return render_template(
        'index.html',        # İşlenecek şablon dosyası
        title='Ana Sayfa',   # HTML'e gönderilen başlık
        user=user,           # HTML'e gönderilen kullanıcı sözlüğü
                             # Soldaki user: Jinja değişkeni
                             # Sağdaki user: Python değişkeni
        posts=posts          # HTML'e gönderilen gönderiler listesi
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
    return redirect(url_for('index'))