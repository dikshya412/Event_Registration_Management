from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import Event
from .forms import EventForm,RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# for event lists
def event_list(request):
    events = Event.objects.all()
    
    return render(request, 'events/event_list.html', {
        'events': events
    })

# for each event details
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    return render(request, 'events/event_detail.html', {
        'event': event
    })

# for creating events
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {
        'form': form
    })

# for editing events 
@login_required
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.organizer != request.user:
        return HttpResponse(
            "You are not allowed to edit this event."
        )

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {
        'form': form,
        'event': event
    })

# for delete 
@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.organizer != request.user:
        return HttpResponse(
            "You are not allowed to delete this event."
        )

    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    
    return render(request, 'events/event_confirm_delete.html', {
        'event': event
    })

# for registration 
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = RegisterForm()

    return render(request, 'events/register.html', {
        'form': form
    })

# for login 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('event_list')
        return render(request, 'events/login.html', {
            'error': 'Invalid username or password.'
        })
    
    return render(request, 'events/login.html')

# for logout
def user_logout(request):
    logout(request)
    return redirect('event_list')

