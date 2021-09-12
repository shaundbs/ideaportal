from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group

# Create your models here.


# create a new user
# create a superuser


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email is a required field")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        group = Group.objects.get(name='admins')
        user.groups.add(group)
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
    return "frontend/imgs/default-avatar-profile-icon-vector-social-media-user-image-182145777.jpg"

class Account(AbstractBaseUser, PermissionsMixin):
    
    AGES_RANGES = [
    ('16-20', '16-20'),
    ('21-30', '21-30'),
    ('31-40', '31-40'),
    ('41-50', '41-50'),
    ('51-65', '51-65'),
    ('65+', '65+'),
]

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    age = models.CharField(choices=AGES_RANGES, max_length=30, default='16-20')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    profile_image=models.ImageField(max_length=255, upload_to= get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    affiliated_with = models.ManyToManyField("organisations.Organisation", related_name='affiliate_tag', null=True)
    # models.ForeignKey("organisation.Organisation", on_delete=models.SET_NULL, related_name='affiliated_with', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_image/{self.pk}/'):]

    def create_user(self, username, email, password):
    # "Create a user and insert into auth_user table"
        if not email:
            raise ValueError("Email is a required field")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user