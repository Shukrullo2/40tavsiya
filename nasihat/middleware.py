from django.http import HttpResponseForbidden

class CustomSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check the Origin header
        origin = request.META.get('HTTP_ORIGIN', '')
        allowed_origin = 'https://40tavsiya.uz'
        
        if request.path.startswith('/api/'):  # Only check for API routes
            if origin != allowed_origin:
                return HttpResponseForbidden('Access denied')
        
        response = self.get_response(request)
        return response 