from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


# -----------------------------
# USER PROFILE
# -----------------------------
class Userprofile(AbstractUser):
    USER_TYPE_CHOICES = [
        ('manager', 'Manager'),
        ('sales_agent', 'Sales Agent'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?\d{10,15}$', 'Enter a valid phone number.')]
    )
    title = models.CharField(max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def is_manager(self):
        return self.user_type == 'manager'

    @property
    def is_salesagent(self):
        return self.user_type == 'sales_agent'

    class Meta:
        db_table = "user_profiles"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

# -----------------------------
# CHICK TYPES
# -----------------------------
class ChickType(models.Model):
    TYPE_CHOICES = [
        ('broiler', 'Broiler'),
        ('layer', 'Layer'),
    ]
    name = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

# -----------------------------
# STOCK MANAGEMENT
# -----------------------------
class Stock(models.Model):
    CHICK_BREED_CHOICES = [
        ('Local', 'Local'),
        ('Exotic', 'Exotic'),
    ]

    chick_breed = models.CharField(max_length=50, choices=CHICK_BREED_CHOICES)
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

# -----------------------------
# FEED STOCK
# -----------------------------
class Feedstock(models.Model):
    FEED_TYPES = [
        ('Starter Feeds', 'Starter Feeds'),
        ('Grower Feeds', 'Grower Feeds'),
    ]
    FEED_BRAND = [
        ('Unga Millers (U) Ltd', 'Unga Millers (U) Ltd'),
        ('Ugachick Poultry Breeders Ltd', 'Ugachick Poultry Breeders Ltd'),
        ('Kaffiika Animal Feeds', 'Kaffiika Animal Feeds'),
        ('Biyinzika Poultry International Limited', 'Biyinzika Poultry International Limited'),
    ]

    feed_name = models.CharField(max_length=100)
    feed_quantity = models.PositiveIntegerField(default=0)
    cost_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    chick_type = models.ForeignKey(ChickType, on_delete=models.SET_NULL, null=True)
    feed_type = models.CharField(max_length=50, choices=FEED_TYPES)
    feed_brand = models.CharField(max_length=100, choices=FEED_BRAND)
    feed_supplier = models.CharField(max_length=250)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.feed_name} - {self.feed_quantity} - {self.feed_type} - {self.selling_price}"

# -----------------------------
# FARMER
# -----------------------------
class Farmer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    FARMER_TYPE_CHOICES = [
        ('Starter', 'Starter'),
        ('Returner', 'Returner'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='farmer_profile',
        null=True,
        blank=True
    )
    farmer_name = models.CharField(max_length=100)
    farmer_age = models.IntegerField()
    farmer_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    farmer_nin = models.CharField(max_length=20)
    farmer_phone_number = models.CharField(max_length=15)
    farmer_type = models.CharField(max_length=50, choices=FARMER_TYPE_CHOICES)
    recomender_name = models.CharField(max_length=100)
    recommender_nin = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.farmer_name} - {self.recomender_name} - {self.farmer_type} - {self.farmer_age}"

    def clean(self):
        if not (18 <= self.farmer_age <= 30):
            raise ValidationError('Farmer age must be between 20 and 30.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# -----------------------------
# CHICK REQUEST
# -----------------------------
class Chickrequest(models.Model):
    CHICK_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    FEED_NEEDED = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    CHICK_DELIVERED = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    farmer_name = models.ForeignKey(Farmer, on_delete=models.SET_NULL, null=True)
    chick_type = models.ForeignKey(ChickType, on_delete=models.SET_NULL, null=True)
    chick_quantity = models.PositiveIntegerField()
    chick_date = models.DateTimeField(auto_now_add=True)
    chick_status = models.CharField(max_length=20, choices=CHICK_STATUS, default='pending')
    feed_needed = models.CharField(max_length=10, choices=FEED_NEEDED)
    chickperiod = models.PositiveIntegerField(default=0)
    chick_delivered = models.CharField(max_length=5, choices=CHICK_DELIVERED, default='no')
    sales_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_requests'
    )

    def __str__(self):
        return f'{self.farmer_name} - {self.chick_type} - {self.chick_quantity} - {self.chickperiod} - {self.chick_status}'

    def clean(self):
        if self.farmer_name is None:
            raise ValidationError("Chick requests must be made by a registered farmer.")
        if self.farmer_name.farmer_type == 'Starter' and self.chick_quantity > 100:
            raise ValidationError("Starter farmers cannot request more than 100 chicks.")
        elif self.farmer_name.farmer_type == 'Returner' and self.chick_quantity > 500:
            raise ValidationError("Returning farmers cannot request more than 500 chicks.")
        if self.chick_status == 'pending':
            four_months_ago = timezone.now() - timedelta(days=120)
            recent_requests = Chickrequest.objects.filter(
                farmer_name=self.farmer_name,
                chick_date__gte=four_months_ago
            )
            if self.pk:
                recent_requests = recent_requests.exclude(pk=self.pk)
            if recent_requests.exists():
                raise ValidationError("You can only request chicks once every 4 months.")

# -----------------------------
# FARMER MESSAGES
# -----------------------------

class FarmerMessage(models.Model):
    sender = models.ForeignKey(
        'Farmer',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)




