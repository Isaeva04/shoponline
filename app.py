from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shop.db'  # файл в котором будет храниться база данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary_key автоматическое проставление порядкового номера
    title = db.Column(db.String(100),nullable=False)
    price =db.Column(db.Integer,nullable=False)
    isActive = db.Column(db.Boolean, default=True)  # активный товар-есть в наличии. True проставляется автоматически
    #text = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/create')
def create():
    return render_template('create.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)