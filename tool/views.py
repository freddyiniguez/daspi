import matplotlib as mpl
mpl.use('Agg')
import os
import glob
import json
import decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project, Estimate, Task, Effort, Cost
from .forms import ProjectForm, EstimateForm, TaskForm, EffortForm, CostForm
from django.contrib import messages
from django.http import Http404, HttpResponse

# Imports for data analysis
import numpy as np 
import pandas as pd 
from numpy.random import randn 

# Imports for stats
from scipy import stats

# Imports for plotting
import matplotlib.pyplot as plt 
import seaborn as sns 
# Imports for Linear Regression
from sklearn import linear_model


# - - - H O M E - - - #
# Home page
def home(request):
	return render(request, 'tool/index.html', {})


# - - - M I L E S T O N E S - - - #
# Milestones and business information about SMART-SPI
def milestones(request):
	return render(request, 'tool/milestones.html', {})


# - - - P R O J E C T S - - - #
# List of current projects for ALL users
@login_required
def projects(request):
	project_list = Project.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(project_list, 2)
	try:
		projects = paginator.page(page)
	except PageNotAnInteger:
		projects = paginator.page(1)
	except EmptyPage:
		projects = paginator.page(paginator.num_pages)
	return render(request, 'tool/projects.html', {'projects' : projects})

# Creates a new project
@login_required
def project_new(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			project = form.save(commit = False)
			project.author = request.user
			project.save()
			messages.success(request, 'Project was successfully created.')
			return redirect('projects_list')
	else:
		form = ProjectForm()
	return render(request, 'tool/project_new.html', {'form' : form})

# Returns project details
@login_required
def project_detail(request, pk):
	project = get_object_or_404(Project, pk=pk)
	# Deletes files from previous visualizations
	files = glob.glob('tool/static/images/visualizations/*')
	for f in files:
		os.remove(f)
	return render(request, 'tool/project_detail.html', {'project' : project})

# Deletes project
def project_delete(request, pk):
	project = get_object_or_404(Project, pk=pk)
	project.delete()
	return redirect('projects_list')


# - - - E S T I M A T E S - - - #
# Creates a new estimate
@login_required
def estimate_new(request, pk):
	if request.method == 'POST':
		form = EstimateForm(request.POST)
		if form.is_valid():
			estimate = form.save(commit = False)
			estimate.project = get_object_or_404(Project, pk=pk)
			estimate.save()
			messages.success(request, 'Estimate was successfully saved.')
			return redirect('project_detail', pk=pk)
	else:
		form = EstimateForm()
	return render(request, 'tool/estimate_new.html', {'form' : form})

# Visualyze estimates information
@login_required
def estimate_visualize(request, pk):
	project = get_object_or_404(Project, pk=pk)

	# Selected targed (attribute) to visualize: "required_hours"
	requirements = tuple(Estimate.objects.only())
	positions = np.arange(len(requirements))
	required_hours = tuple(Estimate.objects.values('required_hours'))
	database = []

	for x in required_hours:
		database.append(x['required_hours'])

	plt.bar(positions, database, align = 'center', alpha = 0.5, color = '#345d9e')
	plt.xticks(positions, requirements, rotation = 'vertical')
	plt.ylabel('Required hours (AVG)')
	plt.title('Required hours per requirement')	
	plt.savefig('tool/static/images/visualizations/estimates.png')
	plt.close()

	# Descriptive analytics
	descriptive = pd.DataFrame(database, columns = ['Required Hours'])
	descriptive_analytics = descriptive.describe()

	return render(request, 'tool/estimate_visualize.html', {'project' : project, 'descriptive' : descriptive_analytics})


# - - - T A S K S - - - #
# Creates a new task
@login_required
def task_new(request, pk):
	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save(commit = False)
			task.project = get_object_or_404(Project, pk=pk)
			task.save()
			messages.success(request, 'Task was successfully saved.')
			return redirect('project_detail', pk=pk)
	else:
		form = TaskForm()
	return render(request, 'tool/task_new.html', {'form' : form})

# Visualyze task information
@login_required
def task_visualize(request, pk):
	project = get_object_or_404(Project, pk=pk)
	# Descriptive Analytics data
	# Selected targed (attribute) to visualize: "task_complexity"
	task_complexity = tuple(Task.objects.values('task_complexity'))
	labels = 'LOW', 'MEDIUM', 'HIGH'
	sizes = []
	low = 0
	medium = 0
	high = 0
	
	for x in task_complexity:
		if (x['task_complexity']=='LOW'):
			low = low + 1
		elif (x['task_complexity']=='MEDIUM'):
			medium = medium + 1
		elif (x['task_complexity']=='HIGH'):
			high = high + 1
	
	sizes.append(low)
	sizes.append(medium)
	sizes.append(high)

	# Linear Regression data
	real_hours = tuple(Task.objects.values('real_hours'))
	time_list = []
	for x in real_hours:
		time_list.append(x['real_hours'])
	time1 = np.array(time_list)
	time = np.reshape(time1, (-1,1))

	real_cost = tuple(Task.objects.values('real_cost'))
	cost_list = []
	for y in real_cost:
		cost_list.append(y['real_cost'])
	cost = np.array(cost_list)
	
	# Descriptive Analytics graphic
	plt.pie(sizes, labels = labels)
	plt.axis('equal')
	plt.title('Task complexity classification')
	plt.savefig('tool/static/images/visualizations/tasks.png')

	plt.clf()

	# Linear Regression graphic
	reg = linear_model.LinearRegression()
	reg.fit(time, cost) # This line makes the Linear Regression model learn from the data
	m = reg.coef_[0]
	b = reg.intercept_
	plt.scatter(time, cost, color = "black")
	predicted_values = [reg.coef_ * i + reg.intercept_ for i in time]
	plt.plot(time, predicted_values, 'b')
	plt.xlabel("Requirement time (in hours)")
	plt.ylabel("Requirement cost")
	plt.title('Task real time vs cost')
	plt.savefig('tool/static/images/visualizations/tasks_prediction.png')

	plt.close()
	
	return render(request, 'tool/task_visualize.html', {'project' : project})

# Predicts cost from an estimated time for a task
@login_required
def task_predict(request):
	if request.is_ajax() and request.POST:
		# Gets data for the Linear Regression model
		real_hours = tuple(Task.objects.values('real_hours'))
		time_list = []
		for x in real_hours:
			time_list.append(x['real_hours'])
		time1 = np.array(time_list)
		time = np.reshape(time1, (-1,1))

		real_cost = tuple(Task.objects.values('real_cost'))
		cost_list = []
		for y in real_cost:
			cost_list.append(y['real_cost'])
		cost = np.array(cost_list)

		# Construct the Linear Rergession model
		reg = linear_model.LinearRegression()
		reg.fit(time, cost) # This line makes the Linear Regression model learn from the data
		m = reg.coef_[0]
		b = reg.intercept_

		# Make prediction with data from user
		D = decimal.Decimal
		predictant = request.POST.get('time')
		predictant = D(predictant)
		result = reg.predict(X=predictant)
		result = round(result.item(0))
		data = {'message': "%s" % result}
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404

# - - - E F F O R T S - - - #
# Creates a new effort
@login_required
def effort_new(request, pk):
	if request.method == 'POST':
		form = EffortForm(request.POST)
		if form.is_valid():
			effort = form.save(commit = False)
			effort.project = get_object_or_404(Project, pk=pk)
			effort.save()
			messages.success(request, 'Effort was successfully saved.')
			return redirect('project_detail', pk=pk)
	else:
		form = EffortForm()
	return render(request, 'tool/effort_new.html', {'form' : form})

# Visualyze effort information
@login_required
def effort_visualize(request, pk):
	project = get_object_or_404(Project, pk=pk)
	# Selected targed (attribute) to visualize: "planned_effort VS real_effort"
	phases = tuple(Effort.objects.only())
	positions = np.arange(len(phases))

	planned = tuple(Effort.objects.values('planned_effort'))
	planned_effort = []

	for x in planned:
		planned_effort.append(x['planned_effort'])

	real = tuple(Effort.objects.values('real_effort'))
	real_effort = []

	for y in real:
		real_effort.append(y['real_effort'])

	fig, ax = plt.subplots()
	index = positions
	bar_width = 0.35
	opacity = 0.8

	rects1 = plt.bar(index, planned_effort, bar_width,
		alpha=opacity,
		color='#345d9e',
		label='Planned effort'
	)

	rects2 = plt.bar(index + bar_width, real_effort, bar_width,
		alpha=opacity,
		color='#9e3449',
		label='Real effort'
	)

	plt.xlabel('Phases')
	plt.ylabel('Effort (in Hours)')
	plt.title('Planned vs Real effort per Phase')
	plt.xticks(index + bar_width, phases, rotation = 'vertical')
	plt.legend()

	plt.tight_layout()
	plt.savefig('tool/static/images/visualizations/efforts.png')
	plt.close()

	# Descriptive analytics
	descriptive_planned = pd.DataFrame(planned_effort, columns = ['Planned Effort'])
	descriptive_analytics_planned = descriptive_planned.describe()
	descriptive_real = pd.DataFrame(real_effort, columns = ['Real Effort'])
	descriptive_analytics_real = descriptive_real.describe()

	return render(request, 'tool/effort_visualize.html', {'project' : project, 'descriptive_planned': descriptive_analytics_planned, 'descriptive_real': descriptive_analytics_real})


# - - - C O S T S - - - #
# Creates a new cost
@login_required
def cost_new(request, pk):
	if request.method == 'POST':
		form = CostForm(request.POST)
		if form.is_valid():
			cost = form.save(commit = False)
			cost.project = get_object_or_404(Project, pk=pk)
			cost.save()
			messages.success(request, 'Cost was successfully saved.')
			return redirect('project_detail', pk=pk)
	else:
		form = CostForm()
	return render(request, 'tool/cost_new.html', {'form' : form})

# Visualyze cost information
@login_required
def cost_visualize(request, pk):
	project = get_object_or_404(Project, pk=pk)
	# Selected targed (attribute) to visualize: "planned_cost VS real_cost"
	phases = tuple(Cost.objects.only())
	positions = np.arange(len(phases))

	planned = tuple(Cost.objects.values('planned_cost'))
	planned_cost = []

	for x in planned:
		planned_cost.append(x['planned_cost'])

	real = tuple(Cost.objects.values('real_cost'))
	real_cost = []

	for y in real:
		real_cost.append(y['real_cost'])

	fig, ax = plt.subplots()
	index = positions
	bar_width = 0.35
	opacity = 0.8

	rects1 = plt.bar(index, planned_cost, bar_width,
		alpha=opacity,
		color='#345d9e',
		label='Planned cost'
	)

	rects2 = plt.bar(index + bar_width, real_cost, bar_width,
		alpha=opacity,
		color='#9e3449',
		label='Real cost'
	)

	plt.xlabel('Phases')
	plt.ylabel('Cost (in Mexican Pesos)')
	plt.title('Planned vs Real cost per Phase')
	plt.xticks(index + bar_width, phases, rotation = 'vertical')
	plt.legend()

	plt.tight_layout()
	plt.savefig('tool/static/images/visualizations/costs.png')
	plt.close()

	# Descriptive analytics
	descriptive_planned = pd.DataFrame(planned_cost, columns = ['Planned Cost'])
	descriptive_analytics_planned = descriptive_planned.describe()
	descriptive_real = pd.DataFrame(real_cost, columns = ['Real Cost'])
	descriptive_analytics_real = descriptive_real.describe()

	return render(request, 'tool/cost_visualize.html', {'project' : project,  'descriptive_planned': descriptive_analytics_planned, 'descriptive_real': descriptive_analytics_real})


# - - - T E M P O R A L - - - #
# A temporal link to see the available HTML theme elements
def help(request):
	return render(request, 'tool/help.html', {})
