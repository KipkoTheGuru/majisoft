from django.db import models
from meter.models import Account

class Invoice(models.Model):
    account = models.ForeignKey(Account)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Invoice"
        
    def __unicode__(self):
        return "%s" % self.account

class InvoiceDetail(models.Model):
    invoice_id = models.ForeignKey("Invoice")
    fee_type = models.ForeignKey("FeeType")
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    
    class Meta:
        db_table = "InvoiceDetail"

class FeeType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = "FeeType"
        
    def __unicode__(self):
        return "%s" % (self.name)

class Payment(models.Model):
    invoice = models.ForeignKey("Invoice")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    cheque_no = models.CharField(max_length=100, blank=True, null = True)
    payment_mode = models.ForeignKey("PaymentMode")
    date_paid = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Payment"

class PaymentMode(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    
    class Meta:
        db_table = "PaymentMode"
        