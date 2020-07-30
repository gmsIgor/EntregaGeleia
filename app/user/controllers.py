from flask import Blueprint, request, render_template, jsonify
from flask_jwt_extended import jwt_required, create_access_token, decode_token
from ..extensions import db
from ..models import User
import bcrypt


user_api = Blueprint('user_api', __name__)


@user_api.route('/user/login/', methods=['POST'])
def login():

    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not data or not email or not password:
        return {'error': 'dados insuficientes'}, 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.checkpw(password.encode(), user.password_hash):
        return {'error': 'dados invalidos'}, 400

    token = create_access_token(identity=user.id)

    return {'token': token}, 201


@user_api.route('/users/', methods=['POST'])
def create():

    data = request.json

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    permission = 'cli' #cliente

    if not name or not email or not password:
        return {'error': 'Dados insuficientes'}, 400

    user_check = User.query.filter_by(email=email).first()

    if user_check:
        return {'error': 'Usuario já cadastrado'}, 400

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user = User(name=name, email=email,
                password_hash=password_hash, permission=permission)

    db.session.add(user)
    db.session.commit()

    return user.json(), 201


@user_api.route('/users/<token>/', methods=['GET'])
def index(token):
    
    data = decode_token(token)

    user_req = User.query.get_or_404(data['identity'])
    if user_req.permission == 'fun' or user_req.permission == 'adm':

        users = User.query.all()

        return jsonify([user.json() for user in users]), 200
    else:
        return {'erro':'você não tem permissão para isso'}, 401


@user_api.route('/users/<int:id>/<string:token>/', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@jwt_required
def user_detail(id,token):
    
    data = decode_token(token)

    user_req = User.query.get_or_404(data['identity'])

    if user_req.permission == 'adm':
        user = User.query.get_or_404(id)

        if request.method == 'GET':
            return user.json(), 200

        if request.method == 'PUT':

            data = request.json

            if not data:
                return {'error': 'Requisição precisa de body'}, 400

            name = data.get('name')
            email = data.get('email')

            if not name or not email:
                return {'error': 'Dados insuficientes'}, 400

            if User.query.filter_by(email=email).first() and email != user.email:
                return {'error': 'Email já cadastrado'}, 400

            user.name = name
            user.email = email

            db.session.add(user)
            db.session.commit()

            return user.json(), 200

        if request.method == 'PATCH':

            data = request.json

            if not data:
                return {'error': 'Requisição precisa de body'}, 400

            email = data.get('email')

            if User.query.filter_by(email=email).first() and email != user.email:
                return {'error': 'Email já cadastrado'}, 400

            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.permission = data.get('permission', user.permission)

            db.session.add(user)
            db.session.commit()

            return user.json(), 200

        if request.method == 'DELETE':
            db.session.delete(user)
            db.session.commit()

            return {}, 204
    else:
        return{'error':'você não tem permissão para isso'}, 401


@user_api.route('/users/activate/<string:token>', methods=['GET'])
def activate(token):

    data = decode_token(token)

    user = User.query.get_or_404(data['identity'])

    if user.active == False:
        user.active = True
        db.session.add(user)
        db.session.commit()

    return render_template('html')
