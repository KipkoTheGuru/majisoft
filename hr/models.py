from django.contrib.auth.models import User
from django.db import models

class Employee(models.Model):
    user = models.ForeignKey(User)
    surname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)
    national_id = models.CharField(max_length=20)
    
    class Meta:
        db_table = "Employee"
    
    def __unicode__(self):
        return self.user.get_full_name()+" %s" % self.surname or self.user.username
    
    @property
    def full_name(self):
        return self.user.get_full_name() + " "+self.surname or employee.user.username
