from event_management.decorators import role_required
from .models import Booking, Role
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
from django.http import JsonResponse
from .forms import BookingForm
from django.shortcuts import render, get_object_or_404, redirect



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



# @login_required
# @role_required(["ADMIN", "MANAGER"])
# def add_event(request):
#     # if request.user.user_role.role not in ["ADMIN", "MANAGER"]:
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Event Created Successfully!")
#             return redirect('event_list')
#         else:
#             print(form.errors)   # Debug in terminal
#     else:
#         form = EventForm()

#     return render(request, 'event_form.html', {
#         'form': form,
#         'form_title': 'Add Event'
#     })

@login_required
@role_required(["ADMIN", "MANAGER"])
def add_event(request):

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return JsonResponse({
                "status": "success",
                "message": "Event Created Successfully!"
            })

        return JsonResponse({
            "status": "error",
            "message": "Invalid Data"
        })

    form = EventForm()
    return render(request, "event_form.html", {
        "form": form,
        "form_title": "Add Event"
    })

# @login_required
# @role_required(["ADMIN"])
# def edit_event(request, id):
#     # if request.user.user_role.role not in ["ADMIN", "MANAGER"]:
#     event = Event.objects.get(id=id)
#     form = EventForm(request.POST or None, instance=event)
#     if form.is_valid():
#         form.save()
#         messages.success(request, "Event Updated Successfully!")
#         return redirect('event_list')
#     return render(request, 'event_form.html', {'form': form, 'form_title': 'Edit Event'})
from django.http import JsonResponse

@login_required
@role_required(["ADMIN"])
def edit_event(request, id):

    event = Event.objects.get(id=id)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            form.save()

            # ✅ If AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    "status": "success",
                    "message": "Event Updated Successfully!"
                })

            # ✅ Normal fallback
            messages.success(request, "Event Updated Successfully!")
            return redirect('event_list')

        # ❌ Validation error
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "status": "error",
                "message": "Invalid form data"
            })

    else:
        form = EventForm(instance=event)

    return render(request, 'event_form.html', {
        'form': form,
        'form_title': 'Edit Event'
    })


# @login_required
# def delete_event(request, id):
#     # if request.user.user_role.role != "ADMIN":
#     event = Event.objects.get(id=id)
#     event.delete()
#     messages.success(request, "Event Deleted Successfully!")
#     return redirect('event_list')
"""AjaxCalling
new way to remove Reload on update"""
@login_required
@role_required(["ADMIN"])
def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()

        return JsonResponse({
            "status": "success",
            "message": "Event Deleted Successfully!"
        })


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
@role_required(["ADMIN", "MANAGER"])
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
# event-detail
@login_required
def event_detail(request, id):
    event = Event.objects.get(id=id)
    return render(request, "event_detail.html", {"event": event})


# Booking
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.save()
            return redirect("my_bookings")
    else:
        form = BookingForm()

    return render(request, "book_event.html", {
        "form": form,
        "event": event
    })

@login_required
def my_bookings(request):
    bookings = request.user.bookings.all()
    booking_count = bookings.count()

    return render(request, "my_bookings.html", {
        "bookings": bookings,
        "booking_count": booking_count
    })

@login_required
def all_bookings(request):
    if request.user.user_role.role != "ADMIN":
        return redirect("event_list")

    bookings = Booking.objects.select_related("user", "event")
    return render(request, "all_bookings.html", {"bookings": bookings})

# update Booking Status
@login_required
def update_booking_status(request, booking_id, status):

    if request.user.user_role.role != "ADMIN":
        return redirect("event_list")

    booking = Booking.objects.get(id=booking_id)
    booking.status = status
    booking.save()

    return redirect("all_bookings")