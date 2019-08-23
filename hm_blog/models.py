from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import string
import random

# Create your models here.

USER_MODEL = settings.AUTH_USER_MODEL


# Common

class Menu(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Footer(models.Model):
    name = models.CharField(max_length=50)
    story = RichTextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class RowMenu(models.Model):
    rowmenu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    footer_rowmenu = models.ForeignKey(Footer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=50, null=True)


class FooterIcons(models.Model):
    icons = models.CharField(max_length=50)
    url = models.CharField(max_length=100)


class Unique(models.Model):
    logo = models.ImageField(upload_to='')
    url = models.CharField(max_length=100, null=True, blank=True)
    copyright = RichTextField(null=True)
    button = models.CharField(max_length=20, null=True)
    Background = models.ImageField(upload_to='', null=True)
    title = models.CharField(max_length=100, null=True)
    subtitle = models.CharField(max_length=200, null=True)
    text = models.TextField(null=True)

    # img = models.ImageField(upload_to='')

    def get_image(self):
        return self.Background.url, self.logo.url

    def __str__(self):
        return f"{self.url}"


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    profile_image = models.ImageField(_('Profile image'), upload_to='', null=True, blank=True)
    headline = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # abstract = True

    def get_image(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return "/static/img/default_avatar.png"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_username(self):
        return self.username

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


User = MyUser


def generate_token(size=120, chars=string.ascii_letters + string.digits):
    return "".join([random.choice(chars) for _ in range(size)])


class Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120, default=generate_token)
    expire = models.BooleanField(default=False)

    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.token}"


class ShotDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Title = models.TextField(null=True, blank=True)
    Preview_image = models.ImageField(upload_to='shotadd/', null=True, blank=True)
    # Images = models.ImageField(upload_to='')
    Description = models.TextField(null=True, blank=True)
    view = models.ManyToManyField(User, related_name="views")
    Lisence = (
        ('Lisence', 'Lisence'),
        ('GPL', 'GPL'),
        ('MIT', 'MIT'),
        ('Apache', 'Apache'),
        ('BSD', 'BSD'),
        ('CCO', 'CCO'),
        ('Other', 'Other')

    )
    tags = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    lisence = models.CharField(max_length=100, choices=Lisence, null=True, blank=True)
    aspect = models.TextField(null=True, blank=True)

    publish_date = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.Title}"

    def get_likers(self):
        return [like.user for like in self.like_set.all()]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    detail = models.ForeignKey(ShotDetails, on_delete=models.CASCADE)
    status = models.IntegerField(choices=(
        (0, 'Like'),
        (1, 'Unlike')
    ),
        default=0
    )

    create_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shot = models.ForeignKey(ShotDetails, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    comment_count = models.PositiveIntegerField(default=0, null=True, blank=True)

    publish_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)



class AddImages(models.Model):
    shotdetail = models.ForeignKey(ShotDetails, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='shotadd/', null=True, blank=True)
    image_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.image.name}"


class SocialSettings(models.Model):
    label = models.CharField(max_length=50, null=True, blank=True)

    def __getitem__(self, item):
        return self.label


class About(models.Model):
    description_about = models.CharField(max_length=255, null=True, blank=True)
    site_story = RichTextField(null=True, blank=True)
    description_about_team = models.CharField(max_length=255, null=True, blank=True)


class AboutTeam(models.Model):
    avatar = models.ImageField(upload_to='', null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    person_story = models.TextField(null=True, blank=True)


class Follow(models.Model):
    from_user = models.ForeignKey(MyUser,
                                  on_delete=models.CASCADE,
                                  related_name='following')
    to_user = models.ForeignKey(MyUser,
                                on_delete=models.CASCADE,
                                related_name='followers')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.from_user} => {self.to_user}'


class ContactUs(models.Model):
    contact = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)


class ContactFormModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
