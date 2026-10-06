from django.shortcuts import render, get_object_or_404,redirect
from .models import Event
from .forms import EventForm

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
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {
        'form': form
    })

# for editing events 
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
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
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {
        'event': event
    })