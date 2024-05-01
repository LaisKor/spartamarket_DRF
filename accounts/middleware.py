from django.http import JsonResponse
from .models import BlacklistedToken

class CheckBlacklistedTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
                if BlacklistedToken.objects.filter(token=token).exists():
                    return JsonResponse({'error': 'Token has been blacklisted'}, status=401)
        response = self.get_response(request)
        return response