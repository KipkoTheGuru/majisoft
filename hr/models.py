from django.contrib.auth.models import User
from django.db import models

class Employee(models.Model):
    user = models.ForeignKey(User)
    sur_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)
    national_id = models.CharField(max_length=20)
    
    class Meta:
        db_table = "Employee"
    
    def __unicode__(self):
        return self.user.get_full_name() or self.user.username
