from django.db import models

class Project(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length = 200)
	company = models.CharField(max_length = 100)
	description = models.TextField()

	def __str__(self):
		return self.title