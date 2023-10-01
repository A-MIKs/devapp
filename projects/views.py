from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import searchProjects, paginate

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects= paginate(request, queryset=projects, results=6)
    context = {"projects": projects, "search_query": search_query, "custom_range": custom_range}
    return render(request, "projects/projects.html", context)


def project(request, pk): 
    project = Project.objects.get(pk=pk)
    form = ReviewForm()
    context = {"project": project, "form": form}

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user.profile
            review.project = project
            review.save()
            project.getVoteCount
            messages.success(request, "Review successfully submitted!")
            return redirect("project", pk=project.id)
        
        else:
            context["form"] = form
            return render(request, "projects/project.html", context)
            
    return render(request, "projects/project.html", context)

@login_required
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("account")
        else:
            messages.error(request, "Error adding project.")
            context["form"] = form
            return render(request, "projects/project_form.html", context)

    context = {"form": form}
    return render(request, "projects/project_form.html", context)

@login_required
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(pk=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")
        else:
            messages.error(request, "An error while updating project.")
            context["form"] = form
            return render(request, "projects/project_form.html", context)

    context = {"form": form}
    return render(request, "projects/project_form.html", context)

@login_required
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(pk=pk)

    if request.method == "POST":
        project.delete()
        return redirect("account")
    
    context = {"object": project.title}
    return render(request, "delete_template.html", context)