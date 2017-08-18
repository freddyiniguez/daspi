from django import forms
from .models import Project, Estimate

class ProjectForm(forms.ModelForm):

	class Meta:
		model = Project
		fields = ('title', 'company', 'description',)

class EstimateForm(forms.ModelForm):

	class Meta:
		model = Estimate
		fields = ('requirement', 'description', 'complexity', 'role', 'required_hours',)