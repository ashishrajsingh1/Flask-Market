from flask_login import UserMixin
from flaskblog import login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=10000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self, **kwargs):
        budget = kwargs.get('budget', self.budget)
        if len(str(budget)) >= 4:
            return f'Rs.{str(budget)[:-3]},{str(budget)[-3:]}'
        else:
            return f"{budget}"

    def check_password_correction(self, attempted_password, **kwargs):
        password_hash = kwargs.get('password_hash', self.password_hash)
        return password_hash == attempted_password

    def can_purchase(self, item_obj, **kwargs):
        budget = kwargs.get('budget', self.budget)
        return budget >= item_obj.price


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user, **kwargs):
        owner = kwargs.get('owner', user.id)
        user.budget -= self.price
        self.owner = owner
        db.session.commit()
