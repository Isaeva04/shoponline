from flask import Flask,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

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

    def __repr__(self):
        return self.title

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html',data=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/create', methods=['POST','GET'])
def create():
    if request.method=='POST':
        title=request.form['title']
        price=request.form['price']
        item=Item(title=title,price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except():
            return "Произошла ошибка"
    else:
        return render_template('create.html')

@app.route('/buy/<int:id>')
def buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "BYN",
        "amount": item.price
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)