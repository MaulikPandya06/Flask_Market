from market import db,login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length=60), nullable=False, unique = True)
    email = db.Column(db.String(length=50), nullable=False, unique = True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), default = 20000)
    items = db.relationship('Item', backref='owned_user', lazy=True) 

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"
    @property
    def can_sell(self, item_obj):
        return item_obj in self.items
    


class Item(db.Model):
      id = db.Column(db.Integer(), primary_key = True)
      name = db.Column(db.String(length=20), nullable=False, unique = True)
      price = db.Column(db.Integer(), nullable=False, unique = True)
      barcode = db.Column(db.String(length=12), nullable=False, unique = True)
      description = db.Column(db.String(length=1024), nullable=False, unique = True)
      owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
      
      def __repr__(self) -> str:
          return f"{self.name}"
        
      def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

      