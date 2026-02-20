from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from .models import Event

urlpatterns = [
       path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',  extra_context={
        "featured_events": Event.objects.all().order_by('-id')[:5]
    }), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', views.event_list, name='event_list'),
    path('', views.landing_page, name='landing'),
    path('add/', views.add_event, name='event_add'),
    path('edit/<id>/', views.edit_event, name='event_edit'),
    path('delete/<id>/', views.delete_event, name='event_delete'),
    #  path('accounts/', include('django.contrib.auth.urls'))
    path('roles/', views.manage_roles, name='manage_roles'),
    path('register/', views.register_view, name='register'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path("book/<int:event_id>/", views.book_event, name="book_event"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("all-bookings/", views.all_bookings, name="all_bookings"),
    path(
    "update-booking/<int:booking_id>/<str:status>/",
    views.update_booking_status,
    name="update_booking_status"
),
]
