from flask import *
from initial import *
from models import User
import smtplib
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

    
@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    if not email.endswith('@kvis-icse.in'):
        print(email)
        flash("Please enter a valid email id!")
        return redirect(url_for('auth.signup'))
    
    name = request.form.get('name')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')
    if password!=cpassword:
        flash("The passwords do not match, please check")
        return redirect(url_for('auth.signup'))
    std = request.form.get('std')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('This email id is already used, please log in or use some other id')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=password, std=int(std))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if user:
        flash('We have successfully created your account. Please log into it to access it')
        return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not user.password==password:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    # print("true!")
    return redirect(url_for('main.ask'))

@auth.route('/reset')
def reset():
    return render_template("reset.html")

@auth.route('/reset', methods=['POST'])
def send_otp():
    email=request.form.get('email')
    sender = 'gandhimanan1810@gmail.com'
    receivers = [email]

    message = "your otp is 1234"

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.sendmail(sender, receivers, message)         
        print("Successfully sent email")
        return render_template('use_otp.html')
    except:
        print("Error: unable to send email")
        return "error"