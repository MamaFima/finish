from django.shortcuts import render

def home(request):
    return render(request, 'base/home.html')

# flowerdelivery_master/views.py
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/register.html'
