from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.home),
	url(r'^milestones/$', views.milestones),
	url(r'^projects/$', views.projects, name = 'projects_list'),
	url(r'^projects/(?P<pk>\d+)/$', views.project_detail, name = 'project_detail'),
	url(r'^projects/new/$', views.project_new, name = 'project_new'),
	url(r'^help/', views.help),
]