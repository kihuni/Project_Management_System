# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as project_views

urlpatterns = [
    path('', project_views.home, name='home'),
    path('register/', project_views.register, name='register'),
    path('login/', project_views.CustomLoginView.as_view(), name='login'),
    path('logout/', project_views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', project_views.profile, name='profile'),
    path('projects/create/', project_views.create_project, name='create_project'),
    path('projects/<int:project_id>/edit/', project_views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/delete/', project_views.delete_project, name='delete_project'),
    path('project/<int:project_id>/', project_views.project_detail, name='project_detail'),
    path('tasks/create/', project_views.create_task, name='create_task'),
    path('tasks/<int:task_id>/edit/', project_views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', project_views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/', project_views.task_detail, name='task_detail'),
]
