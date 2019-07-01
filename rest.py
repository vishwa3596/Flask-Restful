from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from security import authentication, identify
from resources.user import UserRegister
from resources.store import Store,StoreList
from resources.item import Item, ItemList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = 'vishwa'
api = Api(app)


@app.before_first_request
def create_tables():
	db.create_all()


jwt = JWT(app, authentication, identify)  # /auth


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(debug=True)


















