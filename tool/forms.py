from django import forms
from .models import Project, Estimate, Task, Effort

# - - - P R O J E C T - - - #
# Automatically-generated form to create a Project
class ProjectForm(forms.ModelForm):

	class Meta:
		model = Project
		fields = (
			'title',
			'company',
			'description',
		)


# - - - E S T I M A T E - - - #
# Automatically-generated form to create a Estimate
class EstimateForm(forms.ModelForm):

	class Meta:
		model = Estimate
		fields = (
			'requirement',
			'description',
			'complexity',
			'role',
			'required_hours',
		)


# - - - T A S K - - - #
# Automatically-generated form to create a Task
class TaskForm(forms.ModelForm):

	class Meta:
		model = Task
		fields = (
			'task',
			'phase',
			'type',
			'task_complexity',
			'percentage_of_completion',
			'planned_hours',
			'real_hours',
			'planned_cost',
			'real_cost',
			'planned_start_date',
			'planned_end_date',
			'real_start_date',
			'real_end_date',
			'resource',
		)


# - - - E F F O R T - - - #
# Automatically-generated form to create an effort
class EffortForm(forms.ModelForm):

	class Meta:
		model = Effort
		fields = (
			'phase',
			'budgeted_effort',
			'planned_effort',
			'real_effort',
		)