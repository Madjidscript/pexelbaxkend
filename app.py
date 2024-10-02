from flask import Flask # type: ignore
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity # type: ignore
from config.db import *
from flask_restful import Resource, Api # type: ignore
from config.constant import *
from ressources.user import *
from flask_migrate import Migrate  # type: ignore
from flask_cors import CORS # type: ignore
import os

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

app.secret_key = os.urandom(24)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db.init_app(app)

migrate = Migrate(app, db)
api = Api(app)



@app.route('/')
def bienvenue():
    return 'Bienvenue sur mon application Flask !'

api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='all_users',  methods=['GET', 'POST', 'DELETE', 'PATCH'])

if __name__ == '__main__':
    app.run(debug=True)
