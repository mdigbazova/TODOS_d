from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

import pygments
from pygments import highlight # for highlighted code
from pygments.formatters.html import HtmlFormatter # for HTML representation of code
from pygments.lexers import get_all_lexers, get_lexer_by_name
#from pygments.styles import get_all_styles
from multiselectfield import MultiSelectField

# Create your models here.
STATE_CHOICES = (
    (1, 'TO BE DONE'),
    (2, 'PROCESSING'),
    (3, 'RESEARCHING'),
    (4, 'NON-APPLICABLE'),
    (5, 'FAILED'),
    (6, 'FIXED'),
    (7, 'DONE!')
)

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
#STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Todo(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now=True)
    state = MultiSelectField(choices=STATE_CHOICES, default=1)
    end_date = models.DateField(null=True, blank=True) # auto_now=True,
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    code = models.TextField(null=True, blank=True)
    #linenos = models.BooleanField(default=True)
    #style = models.CharField(choices=STYLE_CHOICES, default='solarized-light', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='todos', on_delete=models.CASCADE, null=True) # related_name creates a reverse relationship default=User
    url = models.TextField(blank=True, default='')
    #highlighted = models.TextField(blank=True, default='')

    """
    Requests and Responses
    To be sure that I have restrictions on who can edit or delete todos&code. 

    Todos are always associated with a creator
    Only authenticated users may create todos
    Only the creator of a todo may update or delete it
    Unauthenticated requests should have full read-only access
    """

    class Meta:
        ordering = ('owner', 'state', 'created_date')

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        # lexer = get_lexer_by_name (self.language)
        # linenos = 'table' if self.linenos else False
        # options = {'title': self.title} if self.title else {}
        # formatter = HtmlFormatter (style=self.style, full=True, **options)
        # self.highlighted = highlight (self.code, lexer, formatter)
        super(Todo, self).save(*args, **kwargs)


    def __str__(self):
        """A string representation of the model."""
        return f'{self.owner}:   {self.title} ;   CREATED AT: {self.created_date}.  STATE:  {self.state}. LANGUAGE {self.language}'


#---------------------------


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    profession = models.CharField(max_length=80, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)


    # we are hooking the create_user_profile and save_user_profile methods to the User model,
    # whenever a save event occurs. This kind of signal is called post_save
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def update_profile(request, user_id):
        user = User.objects.get(pk=user_id)
        user.profile.phone_number = request.phone_number
        user.profile.profession = request.profession
        user.profile.location = request.location
        user.save()

    def __str__(self):
        return f'{self.user}'

    # If you will need to access a related data, you can prefetch it in a single database query
    # users = User.objects.all().select_related('profile')

