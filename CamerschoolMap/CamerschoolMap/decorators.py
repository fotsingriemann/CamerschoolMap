from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def login_required_message(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Veuillez vous connecter pour accéder à cette page.")
            return redirect('connexion')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
