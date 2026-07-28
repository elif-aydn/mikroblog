from app import app  # app paketinin içindeki app adlı Flask nesnesini getir.
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm


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
    form = LoginForm()

    if form.validate_on_submit(): #Bu metot iki temel kontrol yapar: 1)İstek form gönderimi mi?, Alanlar doğrulama kurallarını geçiyor mu?
        flash(
            'Login requested for user {}, remember_me={}'.format(
                form.username.data,
                form.remember_me.data
            )
        )
        return redirect(url_for('index'))

    return render_template(
        'login.html',
        title='Sign In',
        form=form
    )