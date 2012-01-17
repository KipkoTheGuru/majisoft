from django.db import models
import nations

IDENTIFICATION=(
        (1, 'National ID'),
        (2, 'Passport'),
)

class Consumer(models.Model):
    NATIONAL_ID = 1
    PASSPORT = 2
    title = models.ForeignKey("Title")
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, blank=True, null = True)
    mobile_no = models.CharField(max_length=50)
    landline_no = models.CharField('Landline', max_length=50, blank=True, null = True)
    email = models.EmailField(blank=True, null = True)
    postal_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null = True)
    town = models.CharField('Town/City', max_length=50)
    id_number = models.CharField('National ID/Passport No', max_length=50, unique=True)
    identification_mode = models.SmallIntegerField(choices=IDENTIFICATION)
    pin_no = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, default='KE', choices=nations.COUNTRIES)
    consumer_type  = models.ForeignKey("ConsumerType")
    company_name = models.CharField(max_length=50, blank=True, null = True)
    nature_of_business = models.TextField(max_length=200, blank=True, null = True)
    date_registered = models.DateField('Date joined', auto_now_add=True)
    
    class Meta:
        db_table = "Consumer"
        
    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.surname, self.other_names)
    
    @property
    def full_name(self):
        return "%s %s, %s %s" % (self.title, self.surname, self.first_name, self.other_names)
    
    @property
    def country_of_origin(self):
        for country in nations.COUNTRIES:
            for chosen_country in country:
                if chosen_country == self.nationality:
                    return country.__getitem__(1)
    
    @property
    def full_address(self):
        if self.postal_code:
            return "%s-%s %s" % (self.postal_address, self.postal_code, self.town)
        return "%s %s" % (self.postal_address, self.town)
        
    @models.permalink
    def get_absolute_url(self):
        return ("consumer-details", [str(self.pk)])

class ConsumerType(models.Model):
    consumer_type = models.CharField(max_length=50)
    
    class Meta:
        db_table = "ConsumerType"
    
    def __unicode__(self):
        return "%s." % self.consumer_type

class Title(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "Title"
        
    def __unicode__(self):
        return "%s." % self.name


class Application(models.Model):
    consumer = models.ForeignKey("Consumer")
    plot_no = models.ForeignKey("Plot")
    service_line_diameter = models.DecimalField(max_digits=10, decimal_places=3)
    approved = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    date_received = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "Application"
        ordering = ['-date_received']
        
    def __unicode__(self):
        return "%s" % self.consumer 
    
    @property
    def service_line(self):
        return "%d mm" % self.service_line_diameter

class Plot(models.Model):
    plot_no = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    landlord = models.ForeignKey("Landlord")
    sub_zone = models.ForeignKey("meter.SubZone", verbose_name='Sub-zone')
    
    class Meta:
        db_table = "Plot"
    
    def __unicode__(self):
        return "%s" % self.plot_no
    
    def plot_location(self):
        return "%s - %s, %s" % (self.street, self.sub_zone.name, self.sub_zone.zone.name)   

class Landlord(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, blank=True, null = True)
    id_number = models.CharField('National ID/Passport No', max_length=50, unique=True)
    identification_mode = models.SmallIntegerField(choices=IDENTIFICATION)
    nationality = models.CharField(max_length=50, default='KE', choices=nations.COUNTRIES)
    name_of_company = models.CharField(max_length=50, blank=True, null = True)
    pin_no = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=50)
    landline_no = models.CharField('Landline', max_length=50, blank=True, null = True)
    postal_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null = True)
    town = models.CharField('Town/City', max_length=50)
    
    class Meta:
        db_table = "Landlord"
    
    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.surname, self.other_names)
    
    @property
    def full_name(self):
        verbose_name = "Consumer / Manager name"
        return "%s, %s %s" % (self.surname, self.first_name, self.other_names)
    
    @property
    def full_address(self):
        if self.postal_code:
            return "%s-%s %s" % (self.postal_address, self.postal_code, self.town)
        return "%s %s" % (self.postal_address, self.town)
    
    @property
    def country_of_origin(self):
        for country in nations.COUNTRIES:
            if country.__get__(0) == self.nationality:
                return "%s" % country.__get__(1)
    
    @models.permalink
    def get_absolute_url(self):
        return ("landlord-details", [str(self.pk)])
    
class Feedback(models.Model):
    FEEDBACK_TYPE=(
        (1, 'Complaint'), 
        (2, 'Suggestion'),
        (3, 'Enquiry'),
    )
    consumer = models.ForeignKey(Consumer)
    feedback_type  = models.SmallIntegerField(choices=FEEDBACK_TYPE)
    description = models.TextField(max_length=500)
    
    class Meta:
        db_table = "Feedback"
        verbose_name_plural = "Feedback"