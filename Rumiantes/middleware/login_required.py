from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = ["/dashboard/","/rumiantes/","/usuarios/","/empresas/",]
    def __call__(self, request):
        path = request.path

        # Skip login, logout, password reset, etc.
        if (
            path.startswith(reverse("login:login"))
            or path.startswith(reverse("login:logout"))
            or path.startswith(reverse("login:home"))
            or path.startswith("/admin/")
        ):
            return self.get_response(request)

        # ✅ Protect only selected paths
        if any(path.startswith(p) for p in self.protected_paths) and not request.user.is_authenticated:
            return redirect(f"{reverse('login:login')}?next={path}")

        return self.get_response(request)
