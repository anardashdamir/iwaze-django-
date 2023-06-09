import imp
from turtle import title
from unittest import result
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import Project, Tag
from django.contrib import messages
from .forms import ProjectForm, ReviewForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .utils import paginateProjects, searchProjects



def projects(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 3)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)


def project(request,pk): 
    project = Project.objects.get(id = pk)
    tags = project.tags.all()
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        project.getVoteCount
        messages.success(request, 'Your review was succesfully submitted!')

        return redirect('project', pk=project.id)



    context = {
        'project': project,
        'tags': tags,
        'form': form,
    }

    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():                  #Save posted datas to db
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')


    context = {
        'form': form
    }
    return render(request, "projects/project_form.html", context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)       # gettin' requested project

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():                  #Save posted datas to db
            
            form.save()
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    
    context = {
        'object':project,
    }
    return render(request, 'delete_template.html', context)
    