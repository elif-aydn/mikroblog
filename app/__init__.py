from flask import Flask #Flask paketinin içindeki Flask sınıfını kullanıma açar.
from config import Config #config.py modülünün içindeki Config sınıfını getirir.

app = Flask(__name__) #Uygulamamızın temel Flask nesnesini oluşturur.
app.config.from_object(Config) #Config sınıfındaki büyük harfle yazılmış yapılandırma değişkenlerini Flask uygulamasına aktarır.
# __name__, Python tarafından otomatik sağlanan özel bir değişkendir. 
# Flask bu bilgi sayesinde uygulamanın hangi modülde bulunduğunu ve şablonlar gibi kaynakları nerede arayacağını belirler.

from app import routes # routes.py dosyasını uygulamaya dâhil eder.