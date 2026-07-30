#SECRET_KEY, Flask’ın güvenlik amacıyla kullandığı gizli anahtardır. Flask-WTF bunu özellikle CSRF koruması için kullanır.
#CSRF saldırısında başka bir site, kullanıcının haberi olmadan senin uygulamana form göndermeye çalışır. 
# Flask-WTF forma tahmin edilmesi zor bir güvenlik belirteci ekler ve form gönderildiğinde bunu kontrol eder.
import os


basedir = os.path.abspath(os.path.dirname(__file__)) #Projenin kök dizininin tam adresini bulur.


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') # DATABASE_URL: İleride farklı bir veritabanı kullanmak istersek ortam değişkeninden adres almamızı sağ
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 25