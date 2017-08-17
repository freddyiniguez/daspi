from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


# - - - H O M E - - -
# Home page
def home(request):
	return render(request, 'tool/index.html', {})


# - - - M I L E S T O N E S - - - 
# Milestones and business information about SMART-SPI
def milestones(request):
	return render(request, 'tool/milestones.html', {})


# - - - P R O J E C T S - - - 
# Projects creation, capture of process information and data analysis and visualization
@login_required
def projects(request):
	projects = Project.objects.all()
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

# - - - T E M P O R A L - - - 
# A temporal link to see the available HTML theme elements
def help(request):
	return render(request, 'tool/help.html', {})