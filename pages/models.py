from django.db import models
from django.conf import settings # For ForeignKey to user
#Extending the super User class for us to create our own users.
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Userprofile(AbstractUser):
    is_salesagent = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    phone = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=5)

    def __str__(self):
        return self.username
# creating a table named farmer users
    class Meta:
        db_table = "farmer_users"
        verbose_name = "User"
        verbose_name_plural = "Users"

class ChickType(models.Model):
    Type_choice = [
        ('broiler', 'Broiler'),
        ('layer', 'Layer'),
    ]
    name = models.CharField(max_length=20, choices=Type_choice, unique=True)

    def __str__(self):
        return self.get_name_display()
class Stock(models.Model):
    stock_name = models.CharField(max_length=200, unique=True)
    quantity = models.PositiveIntegerField()
    chick_type = models.ForeignKey(ChickType, on_delete=models.SET_NULL, null=True)
    chick_breed =[
        ('Local', 'Local'),
        ('Exotic', 'Exotic')
    ]
    chick_breed =  models.CharField(max_length=50, choices=chick_breed)
    chick_price = models.PositiveIntegerField(default=1650)
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    registrername = models.CharField(max_length=200)
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

    feed_type = [
        ('Starter Feeds', 'Starter Feeds'),
        ('Grower Feeds', 'Grower Feeds'),
    ]
    feed_type = models.CharField(max_length=50, choices=feed_type)
    feed_brand =[
    ('Unga Millers (U) Ltd', 'Unga Millers (U) Ltd'),
    ('Ugachick Poultry Breeders Ltd', 'Ugachick Poultry Breeders Ltd'),
    ('Kaffiika Animal Feeds', 'Kaffiika Animal Feeds'),
    ('Biyinzika Poultry International Limited', 'Biyinzika Poultry International Limited'),
   ]
    feed_brand = models.CharField(max_length=100,choices=feed_brand)
    date = models.DateField(auto_now=True)
    feed_supplier = models.CharField(max_length=250)
    selling_price = models.PositiveIntegerField(default=0)
    buying_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.feed_name} - {self.feed_quantity} - {self.feed_type} - {self.selling_price}"

class Farmer(models.Model):
     farmer_name = models.CharField(max_length=100)
     farmer_gender = [('Female','Female'),
              ('Male','Male'),]
     farmer_gender = models.CharField(max_length=10, choices=farmer_gender)
     farmer_nin = models.CharField(max_length=50, unique=True)
     recomender_name = models.CharField(max_length=100)
     recommender_nin = models.CharField(max_length=50)
     farmer_phone_number = models.CharField(max_length=15)
    #  farmer_age(btn 18 and 30)
     Farmer_age = models.PositiveIntegerField()
     farmer_type = [('starter','returning'),
              ('starter','returning'),]
     farmer_type = models.CharField(max_length=20, choices=farmer_type)

     def __str__(self):
        return f"{self.farmer_name} - {self.recomender_name} - {self.farmer_type} -{self.Farmer_age}"

class Chickrequest(models.Model):
    farmer_name = models.ForeignKey(Farmer,on_delete=models.SET_NULL,null=True)
    chick_type = models.ForeignKey(ChickType, on_delete=models.SET_NULL, null=True)
    # >chicks breed
    chick_quantity = models.PositiveIntegerField()
    chick_date = models.DateTimeField(auto_now_add=True)
    chick_status =  [   ('pending', 'Pending'),
                        ('approved', 'Approved'),
                        ('rejected', 'Rejected'),] 
    chick_status = models.CharField(max_length=20, choices=chick_status, default='pending')
    
    feed_needed =[
       ('yes', 'Yes'),
        ('no', 'No'),
    ]
    feed_needed = models.CharField(max_length=10,choices=feed_needed)
    # >chicks period(age in days)
    chickperiod = models.PositiveIntegerField(default=0)
    # >Delivered (y/n) radio button
    chick_delivered = [  ('yes', 'Yes'),
                         ('no', 'No'),
                      ]
    chick_delivered = models.CharField(max_length=5, choices= chick_delivered, default='no')

    def __str__(self):
        return f'{self.farmer_name} - {self.chick_type} - {self.chick_quantity} - {self.chickperiod} - {self.chick_status} - {self.feed_needed}'