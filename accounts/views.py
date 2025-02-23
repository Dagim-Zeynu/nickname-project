from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def complete_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.registration_complete = True
            profile.save()
            return redirect('nicknames:home')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/complete_profile.html', {'form': form}) 