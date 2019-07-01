from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('Price',
						type=float,
						required=True,
						help="This field cannot be left blank"
						)
	parser.add_argument('store_id',
						type=int,
						required=True,
						help="This field cannot be left blank"
						)

	@jwt_required()
	def get(self, name):
		# creating through database
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'item not found'}, 404

	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}

		data = Item.parser.parse_args()

		item = ItemModel(name, data['price'], data['store_id'])
		try:
			item.save_to_db()
		except:
			return {"message": "AN error occured"}, 500

		return item.json(), 201

	def delete(self, name):

		'''
		connection = sqlite3.connect('data.db)
		cursor = connection.connect()

		query = "DELETE FROM items WHERE name=?"
		cursor.execute(query, (name,))

		connection.commit()
		connection.close()
		:param name:
		:return:
		'''
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
			return {'message': 'Item deleted'}
		return {'message': " Item not found "}, 404

	def put(self, name):

		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)

		'''
		updated_item = ItemModel( name, data['price'])
		if item is None:
			try:
				updated_item.insert()
			except:
				return {"messsage": "An error occured "}, 500

		else:
			try:
				updated_item.update()
			except:
				return {"message": "An error occured"}, 500

		return updated_item.json()

		'''
		if item is None:
			item = ItemModel(name, data['price'], data['store_id'])
		else:
			item.price = data['price']

		item.save_to_db()
		return item.json()


class ItemList(Resource):
	def get(self):
		'''
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items"

		result = cursor.execute(query)
		items = []
		for row in result:
			items.append({'name': row[0], 'price': row[1]})

		connection.close()
		:return:
		'''

		return {'items': [item.json() for item in ItemModel.query.all()]}
