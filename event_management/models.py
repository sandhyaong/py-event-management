from django.contrib.auth.models import User
from django.db import models
from djongo import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='events/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    # Role
class Role(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('VIEWER', 'Viewer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_role")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VIEWER')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

    @receiver(post_save, sender=User)
    def create_user_role(sender, instance, created, **kwargs):
     if created:
        Role.objects.create(user=instance)
        
# Booking
class Booking(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_bookings")
    booking_date = models.DateTimeField(default=timezone.now)
    number_of_tickets = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"