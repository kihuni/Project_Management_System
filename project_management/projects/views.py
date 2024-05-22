# projects/views.py

import datetime
from .models import Project, Task
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import TaskForm, ProjectForm
from django.contrib.auth import login


def home(request):
    return render(request, 'projects/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created and logged in as {user.username}!')
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'projects/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'projects/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'home' 

@login_required
def profile(request):
    projects = request.user.project_set.all()
    tasks = request.user.tasks.all()
    completed_tasks = tasks.filter(status='done')
    due_soon_tasks = tasks.filter(due_date__lte=datetime.date.today() + datetime.timedelta(days=7), status__in=['todo', 'in_progress'])
    return render(request, 'projects/profile.html', {
        'projects': projects,
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'due_soon_tasks': due_soon_tasks,
    })


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    return render(request, 'projects/task_detail.html', {'task': task, 'project': project})

# form handling for task creation
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = TaskForm()
    return render(request, 'projects/create_task.html', {'form': form})
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'projects/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('profile')
    return render(request, 'projects/delete_task.html', {'task': task})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('profile')  # Redirect to profile after project creation
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', {'form': form})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('profile')
    return render(request, 'projects/delete_project.html', {'project': project})