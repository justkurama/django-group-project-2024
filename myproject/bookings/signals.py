from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Payment

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        try:
            payment = Payment.objects.get(id=ipn.invoice)
            payment.status = 'Paid'
            payment.paypal_transaction_id = ipn.txn_id
            payment.save()
        except Payment.DoesNotExist:
            pass
    