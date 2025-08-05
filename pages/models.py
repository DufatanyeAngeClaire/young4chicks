
from django.db import models
from django.conf import settings # For ForeignKey to user
#Extending the super User class for us to create our own users.
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.


class Userprofile(AbstractUser):

 USER_TYPE_CHOICES = [
    # ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('sales_agent', 'Sales Agent'),
    # ('farmer', 'Farmer'),
]
 user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

 phone = models.CharField(max_length=15, unique=True, blank=True, null=True, validators=[RegexValidator(r'^\+?\d{10,15}$','Enter a valid phone number.')])
 title = models.CharField(max_length=5, blank=True, null=True)

 class Meta:
        db_table = "user_profiles"
        verbose_name = "User"
        verbose_name_plural = "Users"

 def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class ChickType(models.Model):
    TYPE_CHOICES = [
        ('broiler', 'Broiler'),
        ('layer', 'Layer'),
    ]
    name = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
class Stock(models.Model):
    CHICK_BREED_CHOICES = [
    ('Local', 'Local'),
    ('Exotic', 'Exotic'),
]

    chick_breed =  models.CharField(max_length=50, choices=CHICK_BREED_CHOICES)
    stock_name = models.CharField(max_length=200, unique=True)
    quantity = models.PositiveIntegerField()
    chick_type = models.ForeignKey(ChickType, on_delete=models.SET_NULL, null=True)
    chick_price = models.PositiveIntegerField(default=1650)
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    register_name = models.CharField(max_length=200)
    date_added = models.DateField(auto_now=True)
    chick_age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.stock_name} - {self.quantity} - {self.chick_type} - {self.chick_breed} - {self.chick_age}"


class Feedstock(models.Model):
    feed_name = models.CharField(max_length=100)
    feed_quantity = models.PositiveIntegerField(default=0)
    unit_price = models.PositiveIntegerField()
    cost_price = models.PositiveIntegerField()
    chick_type = models.ForeignKey(ChickType, on_delete=models.SET_NULL, null=True)

    FEED_TYPE = [
        ('Starter Feeds', 'Starter Feeds'),
        ('Grower Feeds', 'Grower Feeds'),
    ]
    feed_type = models.CharField(max_length=50, choices=FEED_TYPE)
    FEED_BRANG =[
    ('Unga Millers (U) Ltd', 'Unga Millers (U) Ltd'),
    ('Ugachick Poultry Breeders Ltd', 'Ugachick Poultry Breeders Ltd'),
    ('Kaffiika Animal Feeds', 'Kaffiika Animal Feeds'),
    ('Biyinzika Poultry International Limited', 'Biyinzika Poultry International Limited'),
   ]
    feed_brand = models.CharField(max_length=100,choices=FEED_BRANG)
    date = models.DateField(auto_now=True)
    feed_supplier = models.CharField(max_length=250)
    selling_price = models.PositiveIntegerField(default=0)
    buying_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.feed_name} - {self.feed_quantity} - {self.feed_type} - {self.selling_price}"

class Farmer(models.Model):
     farmer_name = models.CharField(max_length=100)
     FARMER_GENDER = [('Female','Female'),
              ('Male','Male'),]
     farmer_gender = models.CharField(max_length=10, choices=FARMER_GENDER)
     farmer_nin = models.CharField(max_length=50, unique=True)
     recomender_name = models.CharField(max_length=100)
     recommender_nin = models.CharField(max_length=50)
     farmer_phone_number = models.CharField(max_length=15,validators=[RegexValidator(r'^\+?\d{10,15}$', 'Enter a valid phone number.')])
    #  farmer_age(btn 18 and 30)
     farmer_age = models.PositiveIntegerField()
     FARMER_TYPE = [
    ('starter', 'Starter'),
    ('returning', 'Returning'),
]
     farmer_type = models.CharField(max_length=20, choices=FARMER_TYPE)

     def __str__(self):
        return f"{self.farmer_name} - {self.recomender_name} - {self.farmer_type} -{self.farmer_age}"

class Chickrequest(models.Model):
    farmer_name = models.ForeignKey(Farmer,on_delete=models.SET_NULL,null=True)
    chick_type = models.ForeignKey(ChickType, on_delete=models.SET_NULL, null=True)
    # >chicks breed
    chick_quantity = models.PositiveIntegerField()
    chick_date = models.DateTimeField(auto_now_add=True)
    CHICK_STATUS =  [   ('pending', 'Pending'),
                        ('approved', 'Approved'),
                        ('rejected', 'Rejected'),] 
    chick_status = models.CharField(max_length=20, choices=CHICK_STATUS, default='pending')

    # class Meta:
    #     ordering = ['-chick_date']
    
    FEED_NEEDED =[
       ('yes', 'Yes'),
        ('no', 'No'),
    ]
    feed_needed = models.CharField(max_length=10,choices=FEED_NEEDED)
    # >chicks period(age in days)
    chickperiod = models.PositiveIntegerField(default=0)
    # >Delivered (y/n) radio button
    CHICK_DELIVERED = [  ('yes', 'Yes'),
                         ('no', 'No'),
                      ]
    chick_delivered = models.CharField(max_length=5, choices= CHICK_DELIVERED, default='no')

    def __str__(self):
        return f'{self.farmer_name} - {self.chick_type} - {self.chick_quantity} - {self.chickperiod} - {self.chick_status} - {self.feed_needed}'
pass
