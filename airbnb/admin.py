from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from airbnb import db, app

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('AdminPost', backref='admin', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec) # type: ignore
        return s.dumps({'admin_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            admin_id = s.loads(token)['admin_id']
        except:
            return None
        return Admin.query.get(admin_id)

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"


class AdminPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    picture_1 = db.Column(db.String(20), nullable=False, default='default.jpg')
    picture_2 = db.Column(db.String(20), nullable=False, default='default.jpg')
    picture_3 = db.Column(db.String(20), nullable=False, default='default.jpg')
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __init__(self, title, description, location, price, picture_1=None, picture_2=None, picture_3=None, admin_id=None, category=None):
        self.title = title
        self.description = description
        self.location = location
        self.price = price
        self.picture_1 = picture_1
        self.picture_2 = picture_2
        self.picture_3 = picture_3
        self.admin_id = admin_id
        self.category = category

