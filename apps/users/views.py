from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from apps.users.forms import LoginForm


class LoginView(FormView):
    template_name = 'pages/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        form_data = form.cleaned_data
        user = authenticate(
            username=form_data['username'], password=form_data['password']
        )
        if user:
            login(self.request, user)
            return redirect('builder:schema_list')
        return redirect(reverse('users:login'))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('builder:schema_list')
        return super().get(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect('users:login')