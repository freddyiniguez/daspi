from django.db import models

class Project(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length = 200)
	company = models.CharField(max_length = 100)
	description = models.TextField()

	def __str__(self):
		return self.title

class Estimate(models.Model):
	project = models.ForeignKey('tool.Project', related_name = 'estimates')
	requirement = models.CharField(max_length = 200)
	description = models.TextField()
	# An enum is created to select the complexity of a requirement
	COMPLEXITY_CHOICES = (
		('HIGH', '+30 hours'),
		('MEDIUM', '21-30 hours'),
		('LOW', '0-20 hours'),
	)
	complexity = models.CharField(
		max_length = 20,
		choices = COMPLEXITY_CHOICES,
	)
	# An enum is created to select the role
	ROLE_CHOICES = (
		('LEADER', 'Project Leader'),
		('HARDWARE DEVT', 'Hardware developer'),
		('SOFTWARE DEVT', 'Software developer'),
		('PCB', 'PCB Designer'),
		('TESTER', 'Tester'),
		('IMPLEMENTATOR', 'Implementator'),
		('CONF ADMIN', 'Configuration administrator'),
	)
	role = models.CharField(
		max_length = 30,
		choices = ROLE_CHOICES,
	)
	required_hours = models.FloatField()

	def __str__(self):
		return self.requirement