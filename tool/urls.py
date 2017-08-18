from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.home),
	url(r'^milestones/$', views.milestones),
	url(r'^projects/$', views.projects, name = 'projects_list'),
	url(r'^projects/new/$', views.project_new, name = 'project_new'),
	url(r'^projects/(?P<pk>\d+)/$', views.project_detail, name = 'project_detail'),
	url(r'^projects/(?P<pk>\d+)/delete/$', views.project_delete, name = 'project_delete'),
	url(r'^estimates/(?P<pk>\d+)/new/$', views.estimate_new, name = 'estimate_new'),
	url(r'^estimates/(?P<pk>\d+)/visualize/$', views.estimate_visualize, name = 'estimate_visualize'),
	url(r'^tasks/(?P<pk>\d+)/new$', views.task_new, name = 'task_new'),
	url(r'^tasks/(?P<pk>\d+)/visualize/$', views.task_visualize, name = 'task_visualize'),
	url(r'^help/', views.help),
]