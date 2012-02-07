from django.db import models
from meter.models import Account

class Invoice(models.Model):
    account = models.ForeignKey(Account)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null = True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Invoice"
        
    def __unicode__(self):
        return "%s" % self.account

class InvoiceDetail(models.Model):
    invoice_id = models.ForeignKey("Invoice", blank=True, null = True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default = 1)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null = True)
    
    class Meta:
        db_table = "InvoiceDetail"

class Fee(models.Model):
    INSTALLATION=1
    MONTHLY=2
    PENALTY=3
    FEETYPES = (
        (1, 'Installation Charge'),
        (2, 'Monthly Fee'),
        (3, 'Penalty'),
    )
    name = models.CharField(max_length=50, unique=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    fee_type = models.SmallIntegerField(choices=FEETYPES)
    description = models.TextField(max_length=200)
    
    class Meta:
        db_table = "Fee"
        
    def __unicode__(self):
        return "%s" % (self.name)
    
    @property
    def get_fee_type(self):
        for feetype in self.FEETYPES:
            if self.fee_type == feetype.__getitem__(0):
                return "%s" % feetype.__getitem__(1)

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
    description = models.TextField(max_length=200)
    
    class Meta:
        db_table = "PaymentMode"
        