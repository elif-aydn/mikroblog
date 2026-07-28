from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()]) #Tarayıcıda girilen karakterleri gizleyen bir parola alanı oluşturur. Ancak PasswordField veriyi şifrelemez; yalnızca ekranda maskeler.
    remember_me = BooleanField('Remember Me') #İşaretlenebilen bir onay kutusu oluşturur. Değeri True veya False olur.
    submit = SubmitField('Sign In') #Formu gönderen düğmeyi oluşturur.