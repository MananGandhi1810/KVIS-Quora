from flask import *
from initial import *
from models import User
import smtplib
import random
from flask_login import login_user, logout_user, login_required

email=''
otp=0

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
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login("gandhimanan1810@gmail.com", 'manan123m')
	try:
		server.sendmail('gandhimanan1810@gmail.com', email, "Hello! We have noticed that this email has bee used to sign up for our service, KapolQuora. If this is you ignore this email and enjoy our service, but if it wasn't you, make sure to report it to us at out website https://KapolQuora.mananpyjava.repl.co/report_account")
	except:
		flash('The email id you have submitted is invalid. Please submit a valid email id.')
		return redirect(url_for('auth.signup'))
	if user:
			flash('We have successfully created your account. Please log into it to access it')
			return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = bool(request.form.get('remember'))

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or user.password != password:
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
		global email,otp
		email=request.form.get('email')
		data=User.query.all()
		for x in data:
			print(x.email)
			if email==x.email:
					print(email)
					server = smtplib.SMTP('smtp.gmail.com', 587)
					server.ehlo()
					server.starttls()
					server.login("gandhimanan1810@gmail.com", 'manan123m')
					try:
						otp= random.randint(1000, 9999)
						server.sendmail('gandhimanan1810@gmail.com', email, "Your otp is"+str(otp))
						flash('please check your email, an otp has been sent to you')
						server.close()
						return redirect(url_for('auth.get_otp'))
					except Exception as e:
						print(e)
						flash('Email Could not be sent, please try again after some time.')
						return redirect(url_for('auth.reset'))
		else:
			flash("This email id could not be found on our database")
			return redirect(url_for('auth.reset'))
		
@auth.route('/get_otp')
def get_otp():
	return render_template('use_otp.html')

@auth.route('/get_otp', methods=['POST'])
def check_otp():
    global otp
    input_otp=request.form.get('otp')
    if int(input_otp)==otp:
        return redirect(url_for('auth.newpassword'))
    flash('Wrong OTP!')
    return redirect(url_for('auth.get_otp'))

@auth.route('/newpassword')
def newpassword():
	return render_template('newpass.html')

@auth.route('/newpassword', methods=["POST"])
def newpassword_set():
	global email
	password=request.form.get('password')
	cpassword=request.form.get('cpassword')
	if password==cpassword:
		user=User.query.filter_by(email=email).first()
		user.password=password
		db.session.commit()
		flash('Your password has been updated!')
		return redirect(url_for('auth.login'))
	else:
		flash('The passwords do not match!')
		return redirect(url_for('auth.newpassword'))

@auth.route('/report_account')
def report_account():
	return "Thank you for reporting. You may now close this window."