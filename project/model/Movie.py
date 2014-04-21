from project import db
import datetime

class Movie(db.Document):
	created = db.DateTimeField(default=datetime.datetime.now, required=True)
	title = db.StringField(max_length=255, required=True)
	summary = db.StringField(max_length=10000, required=True)
	tags = db.ListField(db.StringField(max_length=50))
	tmdb_id = db.IntField()
	runtime = db.IntField()
	poster = db.StringField()
	popularity = db.FloatField()

	def addTag(self,tag):
		if tag not in self.tags:
			self.tags.append(tag)
		return self

	def removeTag(self,tag):
		if tag in self.tags:
			self.tags.remove(tag)
		return self    

	def __str__(self):
		return self.title

	def __repr__(self):
		return self.__str__()

	def toJSON(self):
		import json
		return json.dumps({'created': self.created.isoformat(), 'title': self.title, 'summary': self.summary, 'tags': str(self.tags), 'id':str(self.id)})

	@staticmethod
	def convertMovie(movie):
		result = Movie()
		result.tmdb_id = int(movie.id)
		result.title = str(movie.title)
		result.summary = str(movie.overview.encode('utf-8'))
		if movie.poster:
			sizes = movie.poster.sizes()
			if len(sizes) > 0:
				medium = int(len(sizes)/2)
				result.poster = str(movie.poster.geturl(sizes[medium]))
		result.popularity = float(movie.popularity)
		result.runtime = int(movie.runtime)
		tags = movie.keywords
		for tag in tags:
			result.addTag(str(tag))
		genres = movie.genres
		for genre in genres:
			result.addTag(str(genre))
		result.save()
		return result
