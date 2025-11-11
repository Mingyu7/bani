from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # AbstractUser provides: username, first_name, last_name, email,
    # is_staff, is_active, date_joined, etc.

    # We override the email field to make it unique and mandatory for our system.
    email = models.EmailField(unique=True, blank=False)
    nickname = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    profile_image = models.CharField(max_length=255, blank=True, null=True)

    # Resolve reverse accessor clashes with the default User model
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_custom_set",  # Unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_custom_permissions_set",  # Unique related_name
        related_query_name="user",
    )

    # When creating a user via createsuperuser, these fields will be prompted.
    # 'username' and 'password' are required by default.
    REQUIRED_FIELDS = ['email', 'nickname']

    def __str__(self):
        return self.nickname