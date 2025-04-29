from django.urls import resolve
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class OnboardingMiddleware:
    """
    Middleware to redirect authenticated users to onboarding if not completed
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that are exempt from onboarding check
        self.exempt_urls = [
            'api/login/',
            'api/signup/',
            'api/token/refresh/',
            'api/onboarding/',
            'api/categories/'
        ]
    
    def __call__(self, request):
        # Skip middleware for non-authenticated requests
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Check if the current path is in exempt URLs
        current_path = request.path_info
        for exempt_url in self.exempt_urls:
            if exempt_url in current_path:
                return self.get_response(request)
        
        # Check if onboarding is completed
        try:
            if not request.user.userprofile.onboarding_completed:
                # If request is an API request, return JSON response
                if request.path.startswith('/api/'):
                    from rest_framework.renderers import JSONRenderer
                    response_data = {
                        'detail': 'Onboarding not completed',
                        'code': 'onboarding_required'
                    }
                    response = Response(response_data, status=status.HTTP_403_FORBIDDEN)
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = "application/json"
                    response.renderer_context = {}
                    response.render()
                    return response
        except:
            # If userprofile doesn't exist, let the request proceed
            pass
        
        return self.get_response(request)