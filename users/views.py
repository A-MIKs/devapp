from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginate

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles= paginate(request, queryset=profiles, results=6)

    context = {"profiles": profiles, "search_query": search_query, "custom_range": custom_range}
    return render(request, "users/profiles.html", context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {"profile": profile}
    return render(request, "users/user-profile.html", context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect("profiles")

    page = "login"
    context = {"page": page}
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, f"User {username} does not exist.")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else 'account')
        else:
            messages.error(request, "Incorrect cridentials passed")
    return render(request, "users/login_register.html", context)

def logoutUser(request):
    logout(request)
    messages.info(request, "You are now logged out")
    return redirect("login")

def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    context = {"page": page, "form":form}

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Account created successfully!")
            login(request, user)
            return redirect("account")
        else:
            messages.error(request, "An error occurred during registration.")
            context["form"] = form
            return render(request, "users/login_register.html", context)
    return render(request, "users/login_register.html", context)

@login_required
def userAccount(request):
    profile = request.user.profile
    context = {"profile": profile}
    return render(request, "users/account.html", context)

@login_required
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    context = {"form": form}

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account")
        else:
            messages.error(request, "An error occurred while updating your profile.")
            context["form"] = form
            return render(request, "users/login_register.html", context)
    return render(request, "users/profile_form.html", context)

@login_required
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    context = {"form": form}

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "SKill was added successfully")
            return redirect("account")
        else:
            messages.error(request, "Error adding skill.")
            context["form"] = form
            return render(request, "users/skill_form.html", context)
    return render(request, "users/skill_form.html", context)

@login_required
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    context = {"form": form}

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully")
            return redirect("account")
        else:
            messages.error(request, "Error updating skill.")
            context["form"] = form
            return render(request, "users/skill_form.html", context)
        
    return render(request, "users/skill_form.html", context)

@login_required
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(pk=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill deleted successfully")
        return redirect("account")
    
    context = {"object": skill.name}
    return render(request, "delete_template.html", context)


@login_required
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unReadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests": messageRequests, "unReadCount": unReadCount}
    return render(request, "users/inbox.html", context)

@login_required
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)

@login_required
def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    sender = request.user.profile

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.recipient = recipient
            message.name = request.user.profile.name
            message.email = request.user.profile.email
            message.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("profile", pk=recipient.id)
        else:
            messages.error(request, "Error sending message.")
            context["form"] = form
            return render(request, "users/message_form.html", context)


    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)