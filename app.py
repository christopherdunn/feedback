from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost/wine'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'DB'.replace("://", "ql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFCATIONS']=False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    wine = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, wine, rating, comments):
        self.customer = customer
        self.wine = wine
        self.rating = rating
        self.comments = comments



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods= ['POST'])
def submit():
    if request.method =='POST':
        customer = request.form['customer']
        wine = request.form['wine']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, wine, rating, comments)
        if customer == '' or wine == '':
            return render_template('index.html', message='Please fill in all fields')


        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, wine, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, wine, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback!')


if __name__ == '__main__':
    app.run()
