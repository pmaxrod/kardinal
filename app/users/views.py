from django.shortcuts import render
from django.contrib.auth.models import User
from users.forms import UserProfileForm, UserSettingsForm

# Create your views here.
def get_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'user_profile_view.html', {'user': user})

def user_profile_form(request):
    context = {}
    form = UserProfileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    
    context["form"] = form
    return render(request, "user_profile_form.html", context)