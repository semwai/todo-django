from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from project.forms import ProjectForm
from .forms import LoginForm
from .models import UserGroup, Project


# Create your views here.
@login_required(login_url='login')
def index(request):
    user = request.user
    try:
        projects = [ug.project for ug in UserGroup.objects.filter(user_id=user.id)]
    except UserGroup.DoesNotExist:
        projects = None
    form = ProjectForm()
    return render(request, "index.html", {"user": user, "projects": projects, "form": form})


@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return HttpResponse("!!")
        else:
            auth_login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})
