from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, AddFriendForm
from .models import CustomUser, FriendRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login as dlogin, logout
from django.contrib.auth.decorators import login_required
from apps.groups.models import StudyGroup
from apps.questions.models import QuestionRelation
from apps.groups.forms import CreateGroupForm
from apps.groups.services.group_service import create_group
from django.db import IntegrityError
from django.http import JsonResponse

def signup(request):
    #TODO: Cleanup
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                print("Form was valid!")
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    form.add_error('username', 'This LeetCode username is already taken.')
                print("Form was not valid due to unique constraint!")
                print(e)
        else:
            print("Form was not valid!")
            print(form.errors)
            pass
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

def login(request):
    #TODO: This can be cleaned up
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # TODO: Handle logic for if a user doesnt exist. Not sure if this should go here or in the form
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dlogin(request, user)
                return redirect("/accounts/profile/") #TODO: Bugged and will not work
            else:
                form.add_error(None, 'Invalid username or password.')
        else:
            pass
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

#@login_required()
#def profile(request):
#    user = request.user
#    numberOfExcelledQuestions = user.questions.filter(questionrelation__relation_type="excelled").count()
#    numberOfStruggledQuestions = user.questions.filter(questionrelation__relation_type="struggled").count()
#    return render(request, "profile.html", {"user": user, "numberOfExcelledQuestions": numberOfExcelledQuestions, "numberOfStruggledQuestions": numberOfStruggledQuestions })

@login_required()
def profile(request):
    if request.method == "POST":
        clear_messages(request)
        form = AddFriendForm(request.POST)
        if form.is_valid():
            friend_email = form.cleaned_data["friend_email"]
            print("DEBUGGGG")
            print(request.headers.get('x-requested-with'))
            # Prevent sending request to self
            if friend_email == request.user.email:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': "You cannot send a friend request to yourself."})
                messages.error(request, "You cannot send a friend request to yourself.")
                print("CANT SEND TO YOUR SELF")
                return redirect("profile")

            try:
                friend_user = CustomUser.objects.get(email=friend_email)
            except CustomUser.DoesNotExist:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': "No user found with that email."})
                messages.error(request, "No user found with that email.")
                messages.error(request, "No user found with that email.")
                return redirect("profile")

            # Check if already friends
            user = request.user
            friend_user
            if friend_user in user.friends.all():
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': "You are already friends."})
                messages.info(request, "You are already friends.")
                return redirect("profile")

            # Check for an existing pending request
            if FriendRequest.objects.filter(
                    from_user=user, to_user=friend_user, status="pending"
                ).exists():
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': "Friend request already sent."})
                messages.info(request, "Friend request already sent.")
                return redirect("profile")

            # Create and save the friend request
            FriendRequest.objects.create(from_user=user, to_user=friend_user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "Friend request sent!")
            return redirect("profile")
    else:
        form = AddFriendForm()

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
    context = {  "user": user,
                        "numberOfExcelledQuestions": numberOfExcelledQuestions,
                        "numberOfStruggledQuestions": numberOfStruggledQuestions,
                        "group_settings_form": CreateGroupForm(user=user)
                         "form": form }
    return render(request, "profile.html", context)

def clear_messages(request):
    # Clears the messages
    list(messages.get_messages(request))


@login_required
def respond_friend_request(request, request_id, response):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user, status="pending")
    except FriendRequest.DoesNotExist:
        messages.error(request, "Friend request not found.")
        return redirect("profile")

    if response == "accept":
        # Add each other as friends
        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)
        friend_request.delete()
        messages.success(request, "Friend request accepted!")
    elif response == "reject":
        friend_request.delete()
        messages.info(request, "Friend request rejected.")
    else:
        messages.error(request, "Invalid response.")
    
    return redirect("profile")

def settings(request):
    pass

#TODO: Pull out all group logic from profile and put it into the groups app and set up views
# that return the html partials for that view
@login_required()
def logout_view(request):
    logout(request)
    return redirect('login')
