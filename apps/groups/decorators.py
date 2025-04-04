from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import StudyGroup

def owner_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Query through user's study groups using the through model
        membership = request.user.studygroupmembership_set.filter(
            study_group__invite_code=kwargs['invite_code'],
            role="OWNER"
        ).first()
        
        if not membership:
            return HttpResponseForbidden("You are not the owner of this group.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check for either OWNER or ADMIN role
        membership = request.user.studygroupmembership_set.filter(
            study_group__invite_code=kwargs['invite_code'],
            role__in=["OWNER", "ADMIN"]
        ).first()
        
        if not membership:
            return HttpResponseForbidden("You are not an admin of this group.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def belongs_to_group(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        membership = request.user.studygroupmembership_set.filter(
            study_group__invite_code=kwargs['invite_code'],
            role__in=["OWNER", "ADMIN", "MEMBER"]
        ).first()
        
        if not membership:
            return HttpResponseForbidden("You do not belong to this group.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view