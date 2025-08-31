from django.urls import path,reverse
from django.shortcuts import redirect

class RedirectAuthenticatedMiddleware:
    def __init__(self ,response):
        self.get_response=response

    def __call__(self, request):
        target_paths = [reverse("blog:login"), reverse("blog:register")]
        dashboard_path = reverse("blog:dashboard")
        if request.user.is_authenticated and request.path in target_paths:
            if request.path == dashboard_path:
                return self.get_response(request)
            return redirect("blog:dashboard")
        return self.get_response(request)
    
class RestrictUnauthenticatedMiddleware:
    def __init__(self ,response):
        self.get_response = response
    
    def __call__(self, request):
        target_paths = [reverse("blog:dashboard"), reverse("blog:index")]
        index_path = reverse("blog:index")
        if not request.user.is_authenticated and request.path in target_paths:
            if request.path == index_path:
                return self.get_response(request)
            return redirect("blog:index")
        return self.get_response(request)