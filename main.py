from flask import *
from initial import *
from flask_login import login_required, current_user
from models import Questions


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', data=Questions.query.all()[::-1])

@main.route('/', methods=["POST"])
def index_grade():
		std=request.form.get('std')
		if std=="all":
			return redirect(url_for('main.index'))
		return render_template('index.html', data=Questions.query.filter(Questions.std==std).all()[::-1])

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', data=Questions.query.filter(Questions.author==current_user.name).all(), user=current_user.name)

@main.route('/ask')
@login_required
def ask():
    return render_template('ask.html', name=current_user.name)

@main.route('/ask', methods=['POST'])
@login_required
def ask_add():
    question=request.form.get('question')
    description=request.form.get('description')
    std=request.form.get('std')
    q=Questions(question=question, description=description, author=current_user.name, std=std)
    db.session.add(q)
    db.session.commit()
    flash("Question Added!")
    return render_template("ask.html", name=current_user.name)

@main.route('/answer', methods=['POST'])
def answer():
    answer=request.form.get('answer')
    sno=request.form.get('sno')
    change=Questions.query.filter(Questions.sno==sno).first()
    change.answer=answer
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete', methods=['POST'])
def delete_question():
    sno=request.form.get('sno')
    to_delete=Questions.query.filter(Questions.sno==sno).first()
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for('main.profile'))