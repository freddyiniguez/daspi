from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.home),
	url(r'^milestones/', views.milestones),
	url(r'^projects/', views.projects),
]