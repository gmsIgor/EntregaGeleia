from .extensions import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=False)
    permission = db.Column(db.String(3), nullable=False) # permission = adm/cli/fun (administrador/cliente/funcionário)


    def json(self):
        user_json = {'id': self.id,
                     'name': self.name,
                     'email': self.email,
                     'active': self.active,
                     'permission': self.permission}
        return user_json


class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    qtd = db.Column(db.Integer,default=0)
    rate = db.Column(db.Integer, nullable=True)

    def json(self):

        return {'name': self.name,
                'desciption': self.description,
                'id': self.id,
                'price': self.price,
                'qtd': self.qtd,
                'rate': self.rate}
