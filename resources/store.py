from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json()
		return {'message': "store not found"}, 404

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': "a store with name already exists"}
		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {"message": 'error while creating store'}, 500

		return store.json(), 201

	def delete(self):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()

		return {'message': 'store deleted'}


class StoreList(Resource):
	def get(self):
		return {"store": [store.json() for store in StoreModel.query.all()]}
