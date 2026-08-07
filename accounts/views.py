from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import RegisterForm


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


class CustomLogoutView(LogoutView):
    next_page = "home"


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # inicia sesión automáticamente tras registrarse
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})