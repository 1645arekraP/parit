from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm, GroupSettingsForm, AddFriendForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as dlogin, logout
from django.contrib.auth.decorators import login_required
from .models import UserGroup, Profile, Solution, CustomUser, FriendRequest
from .utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from django.http import JsonResponse
from asgiref.sync import sync_to_async
import json

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form was valid!")
        else:
            pass
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})

def login(request):
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
    if request.method == "POST":
        clear_messages(request)
        form = AddFriendForm(request.POST)
        if form.is_valid():
            friend_email = form.cleaned_data["friend_email"]

            # Prevent sending request to self
            if friend_email == request.user.email:
                messages.error(request, "You cannot send a friend request to yourself.")
                print("CANT SEND TO YOUR SELF")
                return redirect("profile")

            try:
                friend_user = CustomUser.objects.get(email=friend_email)
            except CustomUser.DoesNotExist:
                messages.error(request, "No user found with that email.")
                return redirect("profile")

            # Check if already friends
            user_profile = request.user.profile
            friend_profile = friend_user.profile
            if friend_profile in user_profile.friends.all():
                messages.info(request, "You are already friends.")
                return redirect("profile")

            # Check for an existing pending request
            if FriendRequest.objects.filter(
                    from_user=request.user, to_user=friend_user, status="pending"
                ).exists():
                messages.info(request, "Friend request already sent.")
                return redirect("profile")

            # Create and save the friend request
            FriendRequest.objects.create(from_user=request.user, to_user=friend_user)
            messages.success(request, "Friend request sent!")
            return redirect("profile")
    else:
        form = AddFriendForm()

    user = request.user
    numberOfExcelledQuestions = user.profile.questions.filter(questionrelation__relation_type="excelled").count()
    numberOfStruggledQuestions = user.profile.questions.filter(questionrelation__relation_type="struggled").count()
    try:
    # Fetch tags with positive qualityPoints
        positive_tags = user.profile.tag_stats.filter(qualityPoints__gt=0).count.all()

    # Fetch tags with negative qualityPoints
        negative_tags = user.profile.tag_stats.filter(qualityPoints__lt=0).all()

    except AttributeError as e:
        print(f"AttributeError: {e}. Ensure 'user' has a valid profile and related tag stats.")
        positive_tags = []
        negative_tags = []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        positive_tags = []
        negative_tags = []

    return render(request,
                    "profile.html",
                        {  "user": user,
                        "numberOfExcelledQuestions": numberOfExcelledQuestions,
                        "numberOfStruggledQuestions": numberOfStruggledQuestions,
                        "positive_tags": positive_tags,
                        "negative_tags": negative_tags,
                         "form": form }) 
    #user = request.user
    #numberOfExcelledQuestions = user.profile.questions.filter(questionrelation__relation_type="excelled").count()
    #numberOfStruggledQuestions = user.profile.questions.filter(questionrelation__relation_type="struggled").count()
    #return render(request, "profile.html", {"user": user, "numberOfExcelledQuestions": numberOfExcelledQuestions, "numberOfStruggledQuestions": numberOfStruggledQuestions })


@login_required()
def group(request, invite_code):
    user = request.user
    group = UserGroup.userBelongsToGroup(user, invite_code)
    if group:
        print("group valid!")
        if request.method == "POST":
            print("Method was post!")
            form = GroupSettingsForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                print("Saved!")
                return render(request, "group.html", {"user": user, "group": group, "form": form}) 
            else:
                print("Error!")
                pass
        else:
            form = GroupSettingsForm(instance=group)
        return render(request, "group.html", {"user": user, "group": group, "form": form})
    return HttpResponse("Either this group does not exist or you are not in it!")

@login_required()
async def update_group_solutions(request, group_id):
    if request.method == "POST":
        try:
            question_slug = json.loads(request.body)['question_slug']
            user = request.user
            username = await sync_to_async(lambda: user.username)()
            lc_wrapper = LeetcodeWrapper()
            solutions = await lc_wrapper.get_all_solutions(username, limit=5)
            for solution in solutions:
                if solution['titleSlug'] == question_slug:
                    pass
            return JsonResponse({"message": "Update successful", "Response": solutions})
        except Exception as e:
            #print(e)
            return JsonResponse({"error": "Invalid request"}, status=400)
        
@login_required()
def logout_view(request):
    logout(request)
    return redirect('login')

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
        request.user.profile.friends.add(friend_request.from_user.profile)
        friend_request.from_user.profile.friends.add(request.user.profile)
        friend_request.status = "accepted"
        friend_request.save()
        messages.success(request, "Friend request accepted!")
    elif response == "reject":
        friend_request.status = "rejected"
        friend_request.save()
        messages.info(request, "Friend request rejected.")
    else:
        messages.error(request, "Invalid response.")
    
    return redirect("profile")