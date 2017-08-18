from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project, Estimate
from .forms import ProjectForm, EstimateForm, TaskForm


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
	return render(request, 'tool/estimate_visualize.html', {'project' : project})


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
	return render(request, 'tool/task_visualize.html', {'project' : project})


# - - - T E M P O R A L - - - #
# A temporal link to see the available HTML theme elements
def help(request):
	return render(request, 'tool/help.html', {})