#SECRET_KEY, Flask’ın güvenlik amacıyla kullandığı gizli anahtardır. Flask-WTF bunu özellikle CSRF koruması için kullanır.
#CSRF saldırısında başka bir site, kullanıcının haberi olmadan senin uygulamana form göndermeye çalışır. 
# Flask-WTF forma tahmin edilmesi zor bir güvenlik belirteci ekler ve form gönderildiğinde bunu kontrol eder.
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'