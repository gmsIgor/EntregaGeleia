from flask import request, Blueprint, jsonify
from ..models import User, Product
from flask_jwt_extended import jwt_required, decode_token
from ..extensions import db

product_api = Blueprint('product_api', __name__)


@product_api.route('/products/<string:token>/', methods=['POST'])
def create(token):
    
    data = decode_token(token)

    user = User.query.get_or_404(data['identity'])
    
    if user.permission == 'adm' or user.permission == 'fun':
        data = request.json

        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        qtd = data.get('qtd')

        if not data or not name or not description or not price:
            return {'error': 'dados insuficientes'}, 400


        product = Product(name=name, description=description, price=price, qtd=qtd)

        db.session.add(product)
        db.session.commit()

        return product.json(), 201