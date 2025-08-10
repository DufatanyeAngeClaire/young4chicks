from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Chickrequest, Stock

@receiver(pre_save, sender=Chickrequest)
def update_stock_on_approval(sender, instance, **kwargs):
    # If this is a new request (no pk yet), skip
    if not instance.pk:
        return

    # Get the previous saved state of the Chickrequest
    previous = Chickrequest.objects.get(pk=instance.pk)
    
    # Check if status changed from not approved to approved
    if previous.chick_status != 'approved' and instance.chick_status == 'approved':
        # Find stock matching chick_type
        stock = Stock.objects.filter(chick_type=instance.chick_type).first()
        if stock:
            if stock.quantity >= instance.chick_quantity:
                stock.quantity -= instance.chick_quantity
                stock.save()
            else:
                raise ValidationError("Not enough stock to approve this request.")
