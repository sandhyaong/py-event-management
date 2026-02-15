from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date
from django.utils import timezone



# def event_list(request):
#     events = Event.objects.all()
#     return render(request, 'event_list.html', {'events': events})

# def event_list(request):
#     events = Event.objects.all()
#     total = Event.objects.count()
#     upcoming = Event.objects.filter(event_date__gte=date.today()).count()

#     return render(request, 'event_list.html', {
#         'events': events,
#         'total': total,
#         'upcoming': upcoming
#     })
# search
"""def event_list(request):
     events = Event.objects.all()

  search_query = request.GET.get('q')
    if search_query:
         events = events.filter(title__icontains=search_query)

     total = Event.objects.count()
     upcoming = Event.objects.filter(event_date__gte=date.today()).count()

     return render(request, 'event_list.html', {
         'events': events,
         'total': total,
       'upcoming': upcoming
   })"""
# Pagination
@login_required
def event_list(request):
    events = Event.objects.all()

    search_query = request.GET.get('q')
    if search_query:
        events = events.filter(title__icontains=search_query)

    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    total = Event.objects.count()
    upcoming = Event.objects.filter(event_date__gte=date.today()).count()

    return render(request, 'event_list.html', {
        'events': events,
        'total': total,
        'upcoming': upcoming
    })



@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully!")
            return redirect('event_list')
        else:
            print(form.errors)   # Debug in terminal
    else:
        form = EventForm()

    return render(request, 'event_form.html', {
        'form': form,
        'form_title': 'Add Event'
    })

@login_required
def edit_event(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, "Event Updated Successfully!")
        return redirect('event_list')
    return render(request, 'event_form.html', {'form': form, 'form_title': 'Edit Event'})

@login_required
def delete_event(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    messages.success(request, "Event Deleted Successfully!")
    return redirect('event_list')

# Landing page
# def landing_page(request):
#     featured_events = Event.objects.all()[:3]
#     return render(request, "landing.html", {
#         "featured_events": featured_events
#     })
def landing_page(request):
    upcoming_events = Event.objects.filter(
        event_date__gte=timezone.now()
    ).order_by('event_date')

    featured_events = Event.objects.all().order_by('-id')[:3]

    return render(request, 'landing.html', {
        'events': upcoming_events,
        'featured_events': featured_events
    })