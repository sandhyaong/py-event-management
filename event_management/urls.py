from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
       path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', views.event_list, name='event_list'),
    path('', views.landing_page, name='landing'),
    path('add/', views.add_event, name='event_add'),
    path('edit/<id>/', views.edit_event, name='event_edit'),
    path('delete/<id>/', views.delete_event, name='event_delete'),
    #  path('accounts/', include('django.contrib.auth.urls'))
]
