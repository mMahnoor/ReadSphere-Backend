from django.db.models.signals import pre_save
from django.dispatch import receiver
from reservation.models import Reservation

@receiver(pre_save, sender=Reservation)
def set_priority(sender, instance, **kwargs):
    if not instance.id: 
        active_count = Reservation.objects.filter(book=instance.book).count()
        instance.priority = active_count + 1