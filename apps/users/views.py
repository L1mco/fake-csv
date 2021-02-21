from django.contrib.auth import authenticate, login
from django.http import HttpResponse
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
            return HttpResponse('Authenticated successfully')

        return HttpResponse('Invalid login')
