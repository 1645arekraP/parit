from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login as dlogin
from django.contrib.auth.decorators import login_required
from apps.groups.models import StudyGroup
from apps.questions.models import QuestionRelation
from apps.groups.forms import CreateGroupForm
from apps.groups.services.group_service import create_group

def signup(request):
    #TODO: Cleanup
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form was valid!")
        else:
            pass
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

def login(request):
    #TODO: This can be cleaned up
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            print(email, password)
            # TODO: Handle logic for if a user doesnt exist. Not sure if this should go here or in the form
            user = authenticate(email=email, password=password)
            if user is not None:
                dlogin(request, user)
                return redirect("/accounts/profile/") #TODO: Bugged and will not work
            else:
                print(user)
                print("Wrong email or password")
        else:
            pass
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

@login_required()
def profile(request):
    user = request.user
    if request.method == "POST":
        form = CreateGroupForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect("/accounts/profile/")
    else:
        form = CreateGroupForm(user=user)

    numberOfExcelledQuestions = user.questions.filter(questionrelation__relation_type="excelled").count()
    numberOfStruggledQuestions = user.questions.filter(questionrelation__relation_type="struggled").count()
    context = {
        "user": user,
        "numberOfExcelledQuestions": numberOfExcelledQuestions,
        "numberOfStruggledQuestions": numberOfStruggledQuestions,
        "group_settings_form": CreateGroupForm(user=user),
    }
    return render(request, "profile.html", context)

def settings(request):
    pass

#TODO: Pull out all group logic from profile and put it into the groups app and set up views
# that return the html partials for that view