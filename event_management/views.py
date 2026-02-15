from .models import Role
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm



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
    # if request.user.user_role.role not in ["ADMIN", "MANAGER"]:
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
    # if request.user.user_role.role not in ["ADMIN", "MANAGER"]:
    event = Event.objects.get(id=id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, "Event Updated Successfully!")
        return redirect('event_list')
    return render(request, 'event_form.html', {'form': form, 'form_title': 'Edit Event'})

@login_required
def delete_event(request, id):
    # if request.user.user_role.role != "ADMIN":
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
    if request.user.is_authenticated:
        return redirect('event_list')
    upcoming_events = Event.objects.filter(
        event_date__gte=timezone.now()
    ).order_by('event_date')

    featured_events = Event.objects.all().order_by('-id')[:3]

    return render(request, 'landing.html', {
        'events': upcoming_events,
        'featured_events': featured_events
    })
# Role

@login_required
def manage_roles(request):
    if request.user.user_role.role != 'ADMIN':
        return redirect('event_list')

    users = User.objects.all().select_related('user_role')

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        new_role = request.POST.get("role")
          # 🔴 Prevent Admin from changing their own role
        if int(user_id) == request.user.id:
            messages.error(request, "You cannot change your own role!")
            return redirect("manage_roles")
        # 
        role_obj, created = Role.objects.get_or_create(user_id=user_id)
        role_obj.role = new_role
        role_obj.save()

        messages.success(request, "Role Updated Successfully!")

        return redirect("manage_roles")

    return render(request, "manage_roles.html", {"users": users})
# register
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})