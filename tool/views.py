from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project, Estimate, Task, Effort, Cost
from .forms import ProjectForm, EstimateForm, TaskForm, EffortForm, CostForm

# Imports for data analysis
import numpy as np 
import pandas as pd 
from numpy.random import randn 

# Imports for stats
from scipy import stats

# Imports for plotting
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import seaborn as sns 


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
			return redirect('projects_list')
	else:
		form = ProjectForm()
	return render(request, 'tool/project_new.html', {'form' : form})

# Returns project details
@login_required
def project_detail(request, pk):
	project = get_object_or_404(Project, pk=pk)
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

	plt.bar(positions, database, align = 'center', alpha = 0.5)
	plt.xticks(positions, requirements, rotation = 'vertical')
	plt.ylabel('Required hours (AVG)')
	plt.title('Required hours per requirement')	
	plt.savefig('tool/static/images/visualizations/estimates.png')

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
			return redirect('project_detail', pk=pk)
	else:
		form = TaskForm()
	return render(request, 'tool/task_new.html', {'form' : form})

# Visualyze task information
@login_required
def task_visualize(request, pk):
	project = get_object_or_404(Project, pk=pk)
	# Selected targed (attribute) to visualize: "task_complexity"
	return render(request, 'tool/task_visualize.html', {'project' : project})


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
			return redirect('project_detail', pk=pk)
	else:
		form = EffortForm()
	return render(request, 'tool/effort_new.html', {'form' : form})

# Visualyze effort information
@login_required
def effort_visualize(request, pk):
	project = get_object_or_404(Project, pk=pk)
	# Selected targed (attribute) to visualize: "planned_effort VS real_effort"
	return render(request, 'tool/effort_visualize.html', {'project' : project})


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
			return redirect('project_detail', pk=pk)
	else:
		form = CostForm()
	return render(request, 'tool/cost_new.html', {'form' : form})

# Visualyze cost information
@login_required
def cost_visualize(request, pk):
	project = get_object_or_404(Project, pk=pk)
	# Selected targed (attribute) to visualize: "planned_cost VS real_cost"
	return render(request, 'tool/cost_visualize.html', {'project' : project})


# - - - T E M P O R A L - - - #
# A temporal link to see the available HTML theme elements
def help(request):
	return render(request, 'tool/help.html', {})