from django.shortcuts import render

# Home page
def home(request):
	return render(request, 'tool/index.html', {})

# Milestones and business information about SMART-SPI
def milestones(request):
	return render(request, 'tool/milestones.html', {})

# Projects creation, capture of process information and data analysis and visualization
def projects(request):
	return render(request, 'tool/projects.html', {})