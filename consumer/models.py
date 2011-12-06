from django.db import models

class Consumer(models.Model):
    CONSUMER_TYPE=(
        (1, 'Corporate'), 
        (2, 'Domestic'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sur_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    postal_address = models.CharField(max_length=100)
    name_of_company = models.CharField(max_length=50)
    national_id = models.CharField(max_length=50)
    nature_of_business = models.CharField(max_length=50)
    consumer_type  = models.SmallIntegerField(choices=CONSUMER_TYPE)
    title = models.ForeignKey("Title")
    
    class Meta:
        db_table = "Consumer"
        
    def __unicode__(self):
        return "Consumer: #%s, %s %s" % (self.id, self.first_name, self.last_name)

class Title(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "Title"
        
    def __unicode__(self):
        return self.name

class Application(models.Model):
    consumer = models.ForeignKey(Consumer)
    landlord = models.ForeignKey("Landlord")
    approved = models.BooleanField(default=False)
    date_received = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Application"
    
class Landlord(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sur_name = models.CharField(max_length=50)
    postal_address = models.CharField(max_length=100)
    national_id = models.CharField(max_length=50)
    
    class Meta:
        db_table = "Landlord"
        
    def __unicode__(self):
        return "Landlord: #%s, %s %s" % (self.id, self.first_name, self.last_name)
    
class Feedback(models.Model):
    FEEDBACK_TYPE=(
        (1, 'Complaint'), 
        (2, 'Suggestion'),
    )
    consumer = models.ForeignKey(Consumer)
    feedback_type  = models.SmallIntegerField(choices=FEEDBACK_TYPE)
    description = models.CharField(max_length=200)
    
    class Meta:
        db_table = "Feedback"
        