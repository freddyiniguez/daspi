from django.shortcuts import render, get_object_or_404
from .models import Project


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
def projects(request):
	projects = Project.objects.all()
	return render(request, 'tool/projects.html', {'projects' : projects})

# Returns a project details
def project_detail(request, pk):
	project = get_object_or_404(Project, pk=pk)
	return render(request, 'tool/project_detail.html', {'project' : project})

# Creates a new project
def project_new(request):
	return render(request, 'tool/project_new.html', {})


# - - - T E M P O R A L - - - 
# A temporal link to see the available HTML theme elements
def help(request):
	return render(request, 'tool/help.html', {})