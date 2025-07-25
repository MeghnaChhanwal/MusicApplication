import os
from flask import Flask, render_template, Response, jsonify, request,redirect,flash, url_for
from flask import request,flash,redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField,BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo,NumberRange, DataRequired,Email
import gunicorn
from camera import *
from forms import RegisterForm,LoginForm
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import flash
from flask_mail import Mail, Message
from pytube import YouTube
import sqlite3
import cv2
import youtube_dlc as youtube_dl


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/MEGHNA/Downloads/spotify3/song/mydb.db'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # or the appropriate port for your email provider
app.config['MAIL_USERNAME'] = 'turnitupemo@gmail.com'
app.config['MAIL_PASSWORD'] = 'Password@123'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100), unique=True)
    Password = db.Column(db.String(100))
    ConfirmPassword = db.Column(db.String(100))
















  
class RegisterForm(FlaskForm):
   UserName = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
   Password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
   ConfirmPassword = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('Password')])
   Age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=18, max=30, message='Age must be between 18 and 30')])  # Age between 18 and 30
   PhoneNumber = StringField('Phone Number', validators=[InputRequired(), Length(min=10, max=10)])
   Submit = SubmitField('Register')

class LoginForm(FlaskForm):
    UserName = StringField('Username', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Submit = SubmitField('Log In')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
with app.app_context():
    #db.drop_all()
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/camm')
def index():
    print(df1.to_json(orient='records'))
    return render_template('index.html', headings=headings, data=df1)

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

camera = None  # Initialize the camera variable

@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera
    if camera is None:
        camera = VideoCamera()  # Initialize your camera (assuming VideoCamera is your camera class)
        return 'Camera started', 200
    else:
        return 'Camera is already running', 200

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera
    if camera is not None:
        del camera  # Release the camera resource
        camera = None
        return 'Camera stopped', 200
    else:
        return 'No camera is running', 20
    
@app.route('/c')
def c():
    return render_template('cd.html')
@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')



headings = ("Name","Artist","Link")
df1 = music_rec()
df1 = df1.head(10)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/emo')
def emo():
    return render_template('emoji.html')

@app.route('/submit_mood', methods=['POST'])
def submit_mood():
    selected_mood = request.form['selected_mood']

    if selected_mood == '😠':  # Check if the selected mood is '😠' (angry)
        return redirect(url_for('angry'))  # Redirect to the '/happy' route
    if selected_mood == '😢':  # Check if the selected mood is '😢' (sad)
        return redirect(url_for('sad'))  # Redirect to the '/happy' route
    if selected_mood == '😐':  
        return redirect(url_for('neutral'))  
    if selected_mood == '😊':  
        return redirect(url_for('happy'))  
    if selected_mood == '😲':  
        return redirect(url_for('sytr')) 

    # For other moods, redirect to 'play_page' as before
    return redirect(url_for('play_page', mood=selected_mood))


@app.route('/play/<mood>')
def play_page(mood):
    return f'Selected Mood: {mood} <br><a href="/emo">Back to Mood Slider</a>'


def get_entries(playlist_url):
    ydl_opts = {
        'format': 'best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'noplaylist': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        return result.get('entries') if result else None
@app.route('/happy')
def happy():
    playlist_url = 'https://www.youtube.com/playlist?list=PLmQj3u8DC8VuRskKePgLLijK0i78OGeMb'
    videos = get_entries(playlist_url)


    return render_template('happy.html', videos=videos )

@app.route('/sytr')
def sytr():
    playlist_url = 'https://www.youtube.com/playlist?list=PLmQj3u8DC8VuC0GYJ9JewXGOq7ZmrA6mO'
    videos = get_entries(playlist_url)

    return render_template('surprised.html', videos=videos )
@app.route('/neutral')
def neutral():
    playlist_url = 'https://www.youtube.com/playlist?list=PLmQj3u8DC8VsNllU_DnAPw985MpLoM7i2'
    videos = get_entries(playlist_url)

    return render_template('neutral.html', videos=videos )

@app.route('/sad')
def sad():
    playlist_url = 'https://www.youtube.com/playlist?list=PLgvCwzTvwOFg6aFPzBrtxXnbLkXiC7fki'
    videos = get_entries(playlist_url)
    return render_template('sad.html',videos=videos )

    
@app.route('/angry')
def angry():
     playlist_url = 'https://www.youtube.com/playlist?list=PLgvCwzTvwOFg6aFPzBrtxXnbLkXiC7fki'
     videos = get_entries(playlist_url)


     return render_template('angry.html', videos=videos)

@app.route('/seeusers')
def view_users():
    users = User.query.all()  # Fetch all records from the User table
    return render_template('seeusers.html', users=users)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.UserName.data
        password = form.Password.data

        user = User.query.filter_by(UserName=username).first()
        if user and check_password_hash(user.Password, password):
            # Store the user's ID in the session
            #login_user(user, remember=form.remember.data)
            return redirect(url_for('c'))  # Redirect to the 'home' endpoint
        
        return '<h1>Invalid username or password</h1>'
    
    print("Form validation failed.")
    return render_template('login.html', form=form)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user_email = form.email.data

        # Logic to generate a password reset link or token
        # For demonstration, a simple message is sent in the email
        reset_link = "https://your_website/reset_password"  # Replace with your actual reset link

        msg = Message('Password Reset Request', sender='your_email@example.com', recipients=[user_email])
        msg.body = f"Hello! To reset your password, click on this link: {reset_link}"
        mail.send(msg)

        return "Reset password email sent successfully!"

    return render_template('forgot.html', form=form)

@app.route('/registerr', methods=['GET', 'POST'])
def registerr():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.UserName.data
        password = form.Password.data
        confirm_password = form.ConfirmPassword.data

        existing_user = User.query.filter_by(UserName=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('registerr'))

        hashed_password = generate_password_hash(password)
        new_user = User(UserName=username, Password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('dashb'))

    return render_template('register.html', form=form)



@login_manager.user_loader

@app.route('/dashboard')
def dashb():
    return render_template('dashboard.html')

@app.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    app.run()




#sqlite:///C:/Users/MEGHNA/Downloads/spotify3/song/mydb.db