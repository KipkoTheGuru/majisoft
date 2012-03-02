from django.db import models
from django.contrib import admin
from payments.models import *

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["account", "total", "date"]

class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ["invoice_id", "fee", "quantity"]

class FeeAdmin(admin.ModelAdmin):
    list_display = ["name", "fee", "fee_type", "description"]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ["account", "amount_paid", "cheque_no", "payment_mode", "date_paid"]

class PaymentModeAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
        
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceDetail, InvoiceDetailAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentMode, PaymentModeAdmin)
