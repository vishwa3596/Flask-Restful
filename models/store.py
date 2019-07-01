from db import db


class StoreModel(db.Model):
	__tablename__ = 'stores'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	items = db.relationship('StoreModel', lazy="dynamic")

	def __init__(self, name):
		self.name = name

	def json(self):
		return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

	@classmethod
	def find_by_name(cls, name):
		'''
				connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close()
		if row:
			return cls(*row)

		:param name:
		:return:
		'''
		return cls.query.filter_by(name=name).first()

	@classmethod
	def save_to_db(self):
		'''
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "INSERT INTO items VALUES (?,?)"
		cursor.execute(query, (self.name, self.price))
		connection.commit()
		connection.close()
		:return:
		'''
		db.session.add(self)
		db.session.commit()

	@classmethod
	def delete_from_db(self):
		'''
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "UPDATE items SET prices=? WHERE name=?"
		cursor.execute(query, (self.price, self.name))

		connection.commit()
		connection.close()

		:return:
		'''

		db.session.delete(self)
		db.session.commit()
