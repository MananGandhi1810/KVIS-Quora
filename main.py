from flask import *
from initial import db
from flask_login import login_required, current_user
from models import Questions


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', data=Questions.query.all()[::-1])

@main.route('/', methods=["POST"])
def index_grade():
    std=request.form.get('std')
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
    new_answer=Questions.query.filter(Questions.sno==sno).all()
    print(new_answer[0].author)
    question=new_answer[0].question
    description=new_answer[0].description
    author=new_answer[0].author
    std=new_answer[0].std
    new_data=Questions(question=question, description=description, author=author, std=std, answer=answer)
    db.session.add(new_data)
    db.session.commit()
    return redirect(url_for('main.index'))