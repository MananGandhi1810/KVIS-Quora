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
        subject=request.form.get('subject')
        isanswered=request.form.get('answered')
        if std==None or std=="all":
            std="all"
        else: std=int(std)
        if subject==None:
            subject="all"
        if isanswered==None:
            isanswered="all"
        all_data=Questions.query.all()[::-1]
        sorted=[std, subject, isanswered]
        # print(std, subject, isanswered,[x.answer for x in all_data])
        if std=="all" and subject=="all" and isanswered=="all":
            print(1)
            return redirect(url_for('main.index'))
        if std=="all" and subject!="all" and isanswered=="all":
            print(13)
            return render_template('index.html', data=[x for x in all_data if x.subject==subject], sorted=sorted)
        if std!="all" and subject=="all" and isanswered=="all":
            print(14)
            # for x in range(len(all_data)):
                # print(all_data[x].std)
            return render_template('index.html', data=[x for x in all_data if x.std==std], sorted=sorted)
        elif isanswered=="answered" and std!="all" and subject!="all":
            print(5)
            return render_template('index.html', data=[x for x in all_data if x.answer==None and x.std==std and x.subject==subject], sorted=sorted)
        elif isanswered=="answered" and std=="all" and subject!="all":
            print(6)
            return render_template('index.html', data=[x for x in all_data if x.answer!=None and x.subject==subject], sorted=sorted)
        elif isanswered=="answered" and std!="all" and subject=="all":
            print(7)
            return render_template('index.html', data=[x for x in all_data if x.answer==None and x.std==std], sorted=sorted)
        elif isanswered=="unanswered" and std!="all" and subject!="all":
            print(8)
            return render_template('index.html', data=[x for x in all_data if x.answer!=None and x.std==std and x.subject==subject], sorted=sorted)
        elif isanswered=="unanswered" and std=="all" and subject!="all":
            print(9)
            return render_template('index.html', data=[x for x in all_data if x.answer!=None and x.subject==subject], sorted=sorted)
        elif isanswered=="unanswered" and std!="all" and subject=="all":
            print(10)
            return render_template('index.html', data=[x for x in all_data if x.answer!=None and x.std==std], sorted=sorted)
        elif isanswered=="answered" and std=="all" and subject=="all":
            print(11)
            return render_template('index.html', data=[x for x in all_data if x.answer!=None], sorted=sorted)
        elif isanswered=="unanswered":
            print(12)
            return render_template('index.html', data=[x for x in all_data if x.answer==None], sorted=sorted)
        elif std=="all":
            print(2)
            return render_template('index.html', data=[x for x in all_data if x.subject==subject], sorted=sorted)
        elif subject=="all":
            print(3)
            return render_template('index.html', data=[x for x in all_data if x.std==std], sorted=sorted)
        elif isanswered=="all":
            print(4)
            return render_template('index.html', data=[x for x in all_data if x.std==std and x.subject==subject], sorted=sorted)
        

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
    subject=request.form.get('subject')
    q=Questions(question=question, description=description, author=current_user.name, std=std, subject=subject)
    db.session.add(q)
    db.session.commit()
    flash("Question Added!")
    return render_template("ask.html", name=current_user.name)

@main.route('/answer', methods=['POST'])
@login_required
def answer():
    answer=request.form.get('answer')
    no=request.form.get('sno')
    print(no)
    change=Questions.query.filter_by(sno=no).first()
    print(change)
    change.answer=answer
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete', methods=['POST'])
@login_required
def delete_question():
    sno=request.form.get('sno')
    to_delete=Questions.query.filter(Questions.sno==sno).first()
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for('main.profile'))

@main.route('/question/<int:id>')
@login_required
def question_show(id):
    data=Questions.query.filter(Questions.sno==id).first()
    print(data )
    return render_template("question_path.html", data=data)