from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView


class SignupView(CreateView):
    model = User
    template_name = 'tracker/signup.html'
    form_class = UserCreationForm
    success_url = '/' 
