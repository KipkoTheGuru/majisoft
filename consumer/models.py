from django.db import models
import countries

IDENTIFICATION=(
        (1, 'National ID'),
        (2, 'Passport'),
)

class Consumer(models.Model):
    CONSUMER_TYPE=(
        (1, 'Individual'), 
        (2, 'Kiosk'),
        (3, 'Corporate'),
        (4, 'Institutions'),
    )
    
    title = models.ForeignKey("Title")
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, blank=True, null = True)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null = True)
    postal_address = models.CharField(max_length=100)
    identification_mode = models.SmallIntegerField(choices=IDENTIFICATION)
    id_number = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, default='KE', choices=countries.COUNTRIES)
    consumer_type  = models.SmallIntegerField(choices=CONSUMER_TYPE)
    company_name = models.CharField(max_length=50, blank=True, null = True)
    nature_of_business = models.TextField(max_length=200, blank=True, null = True)
    
    class Meta:
        db_table = "Consumer"
        
    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.surname, self.other_names)
    
    @property
    def full_name(self):
        return "%s %s, %s %s" % (self.title, self.surname, self.first_name, self.other_names)
        
    @models.permalink
    def get_absolute_url(self):
        return ("consumer-details", [str(self.pk)])

class Title(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "Title"
        
    def __unicode__(self):
        return "%s." % self.name

class Application(models.Model):
    consumer = models.ForeignKey("Consumer")
    landlord = models.ForeignKey("Landlord")
    approved = models.BooleanField(default=False)
    date_received = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Application"
    
class Landlord(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, blank=True, null = True)
    id_number = models.CharField(max_length=50)
    identification_mode = models.SmallIntegerField(choices=IDENTIFICATION)
    nationality = models.CharField(max_length=50, default='KE', choices=countries.COUNTRIES)
    name_of_company = models.CharField(max_length=50, blank=True, null = True)
    pin_no = models.CharField(max_length=50)
    postal_address = models.CharField(max_length=100)
    plot_no = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    
    class Meta:
        db_table = "Landlord"
    
    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.surname, self.other_names)
    
    @property
    def full_name(self):
        return "%s, %s %s" % (self.surname, self.first_name, self.other_names)
    
class Feedback(models.Model):
    FEEDBACK_TYPE=(
        (1, 'Complaint'), 
        (2, 'Suggestion'),
        (3, 'Query'),
    )
    consumer = models.ForeignKey(Consumer)
    feedback_type  = models.SmallIntegerField(choices=FEEDBACK_TYPE)
    description = models.TextField(max_length=500)
    
    class Meta:
        db_table = "Feedback"
        