from project import db
import User, sys

class Library(db.Document):
	user = db.ReferenceField(User.User)
	unit = db.StringField(max_length=50) #what Document the Library's collection relates to 
	name = db.StringField(max_length=100, unique_with=['user','unit']) #name of the Library
	lookup_attribute = db.StringField(default='_id')
	collection = db.ListField(db.StringField())
	summary = db.StringField()

	def get_class(self, kls ):
		parts = kls.split('.')
		module = ".".join(parts[:-1])
		m = __import__( kls )
		for comp in parts[1:]:
			print comp
			m = getattr(m, comp)            
		return m

	def addUnit(self,unit):
		if self.unit == type(unit).__name__:
			self.collection.append("%s" % unit.id)
		else:
			raise Exception("Cannot add %s to Library of %s" % (type(unit).__name__,self.unit))    		
		return self

	# @param index --represents the index in the Library collection of the object
	def getUnit(self, index):
		if index < 0 or index > self.collection.count:
			raise Exception("Invalid index for Library %s" % self.name)
		attr = {}
		attr[self.lookup_attribute] = self.collection[index]
		print attr
		# m = get_class("project.models.%s"%self.unit)
		model =  getattr(sys.modules["project.models.%s"%self.unit], self.unit)
		# return model(attr)
		return model(**model._get_collection().find_one(**attr))