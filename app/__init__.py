from flask import Flask, logging #Flask paketinin içindeki Flask sınıfını kullanıma açar.
from flask_sqlalchemy import SQLAlchemy #Flask-SQLAlchemy paketinin içindeki SQLAlchemy sınıfını kullanıma açar.
from flask_migrate import Migrate #Flask-Migrate paketinin içindeki Migrate sınıfını kullanıma açar.
from flask_login import LoginManager

from config import Config #config.py modülünün içindeki Config sınıfını getirir.
from flask_mail import Mail #Flask-Mail paketinin içindeki Mail sınıfını kullanıma açar.

app = Flask(__name__) #Uygulamamızın temel Flask nesnesini oluşturur.
app.config.from_object(Config) #Config sınıfındaki büyük harfle yazılmış yapılandırma değişkenlerini Flask uygulamasına aktarır.
# __name__, Python tarafından otomatik sağlanan özel bir değişkendir. 
# Flask bu bilgi sayesinde uygulamanın hangi modülde bulunduğunu ve şablonlar gibi kaynakları nerede arayacağını belirler.

db = SQLAlchemy(app) #SQLAlchemy sınıfının bir örneğini oluşturur ve Flask uygulamasına bağlar.
migrate = Migrate(app, db) #Migrate sınıfının bir örneğini oluşturur ve Flask uygulaması ile SQLAlchemy veritabanına bağlar.
login = LoginManager(app) #LoginManager sınıfının bir örneğini oluşturur ve Flask uygulamasına bağlar.
login.login_view = 'login'
mail = Mail(app)

from app import routes, models, errors # routes.py, models.py ve errors.py dosyalarını uygulamaya dâhil eder.
