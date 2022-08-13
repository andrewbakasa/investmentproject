from django.db.models.signals import pre_delete
from .models import InvoiceAttachment, ExpenseAttachment
from store.models import OrderAttachment 

def delete_invoice_image(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.file:
        instance.file.delete(False)

pre_delete.connect(delete_invoice_image, sender=InvoiceAttachment)


def delete_expense_image(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.file:
        instance.file.delete(False)

pre_delete.connect(delete_expense_image, sender=ExpenseAttachment)

def delete_order_image(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.file:
        instance.file.delete(False)
pre_delete.connect(delete_order_image, sender=OrderAttachment)


from .models import ClientReportAttachment

def delete_clientreport_image(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.file:
        instance.file.delete(False)

pre_delete.connect(delete_clientreport_image, sender=ClientReportAttachment)


