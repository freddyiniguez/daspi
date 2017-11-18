from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# - - - P R O J E C T - - - #
# Contains information about the project, a title, a company and a short description.
class Project(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length = 200)
	company = models.CharField(max_length = 100)
	description = models.TextField()

	def __str__(self):
		return self.title


# - - - E S T I M A T E - - - #
# From the Project Planning process, an estimates contains information about requirements and its duration.
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


# - - - T A S K - - - #
# From the Monitoring and Control process, a task contains information about planned vs real hours, percentage of completion and resources to developed.
class Task(models.Model):
	project = models.ForeignKey('tool.Project', related_name = 'tasks')
	# An enum is created to select a specific phase within the task
	PHASE_CHOICES = (
		('START', 'Starting'),
		('REQM', 'Requirements'),
		('PLAN', 'Planning'),
		('DEVT', 'Development'),
		('TEST', 'Testing'),
		('IMPLEMENTATION', 'Implementation'),
		('CONTROL', 'Monitoring and control'),
		('CONFIG', 'Configuration management'),
		('CLOSURE', 'Closure'),
	)
	phase = models.CharField(
		max_length = 100,
		choices = PHASE_CHOICES,
	)
	task = models.TextField()
	# An enum is created to select a specific type of task
	TYPE_CHOICES = (
		('REQM', 'Requirement'),
		('TASK', 'Task'),
		('CHANGE', 'Changes'),
	)
	type = models.CharField(
		max_length = 20,
		choices = TYPE_CHOICES,
	)
	# An enum is created to select the complexity of a task
	COMPLEXITY_CHOICES = (
		('VERY HIGH', 'Very high'),
		('HIGH', 'High'),
		('MEDIUM', 'Medium'),
		('LOW', 'Low'),
		('VERY LOW', 'Very low')
	)
	task_complexity = models.CharField(
		max_length = 20,
		choices = COMPLEXITY_CHOICES,
	)
	percentage_of_completion = models.IntegerField(
		validators = [
			MaxValueValidator(100),
			MinValueValidator(1),
		]
	)
	planned_hours = models.FloatField()
	real_hours = models.FloatField()
	planned_cost = models.FloatField()
	real_cost = models.FloatField()
	planned_start_date = models.DateField()
	planned_end_date = models.DateField()
	real_start_date = models.DateField(blank = True, null = True)
	real_end_date = models.DateField(blank = True, null = True)
	# An enum is created to select a specific resource (person) for a task
	RESOURCE_CHOICES = (
		('MAURICIO', 'Mauricio Mendonza'),
		('HECTOR', 'Hector Guerrero'),
		('GERARDO', 'Gerardo'),
		('JOSHUA', 'Joshua Mendonza'),
		('ANTONIO', 'Antonio Nava'),
	)
	resource = models.CharField(
		max_length = 50,
		choices = RESOURCE_CHOICES,
	)

	def __str__(self):
		return self.task


# - - - E F F O R T - - - #
# From the Monitoring and Control process, an effort constains information for planned and real effort 
class Effort(models.Model):
	project = models.ForeignKey('tool.Project', related_name = 'efforts')
	# An enum is created to select a specific phase within the effort
	PHASE_CHOICES = (
		('START', 'Starting'),
		('REQM', 'Requirements'),
		('PLAN', 'Planning'),
		('DEVT', 'Development'),
		('TEST', 'Testing'),
		('IMPLEMENTATION', 'Implementation'),
		('CONTROL', 'Monitoring and control'),
		('CONFIG', 'Configuration management'),
		('CLOSURE', 'Closure'),
	)
	phase = models.CharField(
		max_length = 100,
		choices = PHASE_CHOICES,
	)
	budgeted_effort = models.FloatField()
	planned_effort = models.FloatField()
	real_effort = models.FloatField()

	def deviation_budgeted_planned(self):
		deviation = self.planned_effort - self.budgeted_effort
		if (self.budgeted_effort > 0):
			deviation = (deviation / self.budgeted_effort) * 100
			deviation = round(deviation, 2)
		else:
			deviation = 0
		return deviation

	def deviation_planned_real(self):
		deviation = self.real_effort - self.planned_effort
		if (self.planned_effort > 0):
			deviation = (deviation / self.planned_effort) * 100
			deviation = round(deviation, 2)
		else:
			deviation = 0
		return deviation

	def __str__(self):
		return self.phase


# - - - C O S T - - - #
# From the Monitoring and Control process, a cost constains information for planned and real cost
class Cost(models.Model):
	project = models.ForeignKey('tool.Project', related_name = 'costs')
	# An enum is created to select a specific phase within the cost
	PHASE_CHOICES = (
		('START', 'Starting'),
		('REQM', 'Requirements'),
		('PLAN', 'Planning'),
		('DEVT', 'Development'),
		('TEST', 'Testing'),
		('IMPLEMENTATION', 'Implementation'),
		('CONTROL', 'Monitoring and control'),
		('CONFIG', 'Configuration management'),
		('CLOSURE', 'Closure'),
	)
	phase = models.CharField(
		max_length = 100,
		choices = PHASE_CHOICES,
	)
	budgeted_cost = models.FloatField()
	planned_cost = models.FloatField()
	real_cost = models.FloatField()

	def deviation_budgeted_real(self):
		deviation = self.real_cost - self.budgeted_cost
		if (self.budgeted_cost > 0):
			deviation = (deviation / self.budgeted_cost) * 100
			deviation = round(deviation, 2)
		else:
			deviation = 0
		return deviation

	def deviation_planned_real(self):
		deviation = self.real_cost - self.planned_cost
		if (self.planned_cost > 0):
			deviation = (deviation / self.planned_cost) * 100
			deviation = round(deviation, 2)
		else:
			deviation = 0
		return deviation

	def __str__(self):
		return self.phase
