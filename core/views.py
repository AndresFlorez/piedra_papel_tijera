from django.conf import settings
from django.contrib.auth import (authenticate, login, user_logged_in,
                                 user_logged_out, user_login_failed)
from django.shortcuts import redirect, render

from core.auth_form.form import UCF


def signup(request):
    if request.method == 'POST':
        form = UCF(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            redirect_to = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
            return redirect(redirect_to)
    else:
        form = UCF()
    return render(request, 'registration/signup.html', {'form': form})

def logout(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if not getattr(user, 'is_authenticated', True):
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)
    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    return render(request, 'registration/logout.html', {})
