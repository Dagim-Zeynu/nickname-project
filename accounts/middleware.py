from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            '/admin/',
            '/accounts/complete-profile/',
            '/accounts/login/',
            '/accounts/google/login/',
            '/accounts/google/login/callback/',
            '/accounts/logout/',
            '/static/',
        ]

        # Skip middleware for exempt URLs
        if any(request.path.startswith(url) for url in exempt_urls):
            return self.get_response(request)

        # Check if user is authenticated
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                if not profile.registration_complete:
                    if not request.path.startswith('/accounts/complete-profile/'):
                        messages.warning(request, 'Please complete your profile first.')
                        return redirect('accounts:complete_profile')
            except AttributeError:
                if not request.path.startswith('/accounts/complete-profile/'):
                    return redirect('accounts:complete_profile')

        response = self.get_response(request)
        return response 