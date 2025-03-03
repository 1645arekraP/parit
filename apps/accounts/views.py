from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login as dlogin
from django.contrib.auth.decorators import login_required
from apps.groups.models import StudyGroup
from apps.questions.models import QuestionRelation

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
    numberOfExcelledQuestions = user.questions.filter(questionrelation__relation_type="excelled").count()
    numberOfStruggledQuestions = user.questions.filter(questionrelation__relation_type="struggled").count()
    return render(request, "profile.html", {"user": user, "numberOfExcelledQuestions": numberOfExcelledQuestions, "numberOfStruggledQuestions": numberOfStruggledQuestions })

def settings(request):
    pass