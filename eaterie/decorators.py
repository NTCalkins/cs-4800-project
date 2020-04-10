from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from eaterie.models import CustomUserModel, Restaurant


def restaurant_owner_identity_check(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        owner = get_object_or_404(Restaurant, pk=kwargs['pk'])
        if owner == request.user.restaurant:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_identity_check(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = get_object_or_404(CustomUserModel, pk=kwargs['pk'])
        if user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def customer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    '''
    Decorator for views that checks that the logged in user is a customer,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_customer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def restaurant_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    '''
    Decorator for views that checks that the logged in user is a restaurant,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_restaurant,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
