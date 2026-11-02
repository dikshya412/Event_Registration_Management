from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import OrganizerRequestForm
from .models import OrganizerRequest

@login_required
def organizer_request(request):
    # only students can request orgainzer access
    if request.user.profile.role == 'organizer':
        messages.info(request,"you are already an organizer.")
        return redirect('event_list')

    # prevent multiple pending requests
    pending_request = OrganizerRequest.objects.filter(
        user=request.user,
        status = 'pending'
    ).exists()

    if pending_request:
        messages.info(request,"you already have a pending organizer request.")
        return redirect('event_list')
    
    if request.method == 'POST':
        form = OrganizerRequestForm(request.POST)
        if form.is_valid():
            organizer_request = form.save(commit=False)  #creates model obj without saving it immediately
            # Assign the currently logged-in user
            organizer_request.user = request.user
            organizer_request.save()
            messages.success(
                request,
                "Your organizer request has been submitted successfully."
            )
            return redirect('event_list')
    else:
        form = OrganizerRequestForm()
    return render(request, 'accounts/organizer_request.html', {
        'form': form
    })