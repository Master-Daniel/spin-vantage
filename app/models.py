import logging
import secrets

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Get an instance of a logger
logger = logging.getLogger(__name__)

class UserProfile(models.Model):
    """
    Class to represent user profiles with a one-to-one relationship to the User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)  # Full name field
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)

class Deposit(models.Model):

    user = models.CharField(blank=False, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    method = models.CharField(max_length=255)

class Draw(models.Model):
    """
    Class to represent each valid draw that happened in the system.
    """
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="draws", null=True, blank=True)
    email = models.EmailField(blank=False)
    code = models.CharField(max_length=8)
    sent = models.BooleanField(default=False)
    rotation = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True, null=True)
    prize = models.ForeignKey('Prize', on_delete=models.CASCADE, null=False, blank=False)
    retry_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code}"

    def use_retry(self):
        self.retry_used = True
        self.save()


class UniqueCode(models.Model):
    """
    Class to create human friendly gift/coupon/voucher codes.
    """
    # Model field for our unique code
    code = models.CharField(max_length=8, blank=True, null=True, unique=True, default="Automatic Generated", editable=False)
    used = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    prize = models.ForeignKey('Prize', on_delete=models.CASCADE, null=True, blank=True, default=None)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        """
        Connected to the post_save signal of the UniqueCodes model. This is used to set the
        code once we have created the db instance and have access to the primary key (ID Field).
        """
        # If new database record
        if created:
            # We have the primary key (ID Field) now so let's grab it
            id_string = str(instance.id)
            # Define our random string alphabet
            # (notice I've omitted I,O,etc. as they can be confused for other characters)
            upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
            # Create an 8 char random string from our alphabet
            random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
            # Append the ID to the end of the random string
            instance.code = (random_str + id_string)[-8:]
            # Save the class instance
            instance.save()

    def __str__(self):
        return f"{self.code} [Used: {self.used}]"


# Connect the post_create function to the UniqueCodes post_save signal
post_save.connect(UniqueCode.post_create, sender=UniqueCode)


class Prize(models.Model):
    """
    Class to represent each available prize in the wheel.
    """
    label = models.CharField(max_length=12)
    winner = models.BooleanField(default=False)
    try_again = models.BooleanField(default=False)

    def __str__(self):
        return self.label
