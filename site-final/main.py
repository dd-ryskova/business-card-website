from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/Users/drysk/OneDrive/Рабочий стол/Моя папка/5 семестр/ТП/site-final/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    comment_text = db.Column(db.Text(), nullable=False)
    commentator_name = db.Column(db.Text(), nullable=False)

    def __init__(self, _name, _text):
        self.commentator_name = _name
        self.comment_text = _text


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/menu')
def menu():
    return render_template("menu.html")


@app.route('/sale')
def sale():
    return render_template("sale.html")


@app.route('/comments', methods=['POST', 'GET'])
def comments():
    if request.method == 'POST':
        name = request.form['name']
        text = request.form['text']
        comm = None
        if name != '' and text != '':
            comm = Comment(_text=text, _name=name)
        else:
            flash("Поля не должны быть пустыми!")
            return redirect('/comments')
        try:
            db.session.add(comm)
            db.session.commit()
        except:
            flash("Неизвестная ошибка, обратитесь к администратору")
    comms = Comment.query.order_by(Comment.comment_id.desc()).all()
    return render_template("comments.html", comms=comms)


@app.route('/vacancy')
def vacancy():
    return render_template("vacancy.html")


@app.route('/partners')
def partners():
    return render_template("partners.html")


@app.route('/delivery')
def delivery():
    return render_template("delivery.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.secret_key = 'superpuperbibaboba'
    app.run()
