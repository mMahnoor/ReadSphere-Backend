from django.db import models
from users.models import CustomUser
from book.models import Book
from django.utils import timezone

# Create your models here.
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    )

    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reservations")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reservations")
    reservation_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['member', 'book'], name="unique_reservation_pair"
            )
        ]

    def __str__(self):
        return f"Reservation: {self.book.title} by {self.member.username} ({self.status})"
