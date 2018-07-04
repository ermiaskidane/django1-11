from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from .utils import code_generator
from django.core.mail import send_mail

from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL
# Create your models here.
class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following

class Profile(models.Model):
    user            = models.OneToOneField(User)    #user.profile
    followers       = models.ManyToManyField(User, related_name="is_following", blank=True)  #user.is_following.all()  #user.profile_set.all()
    # following       = models.ManyToManyField(User, related_name="following", blank=True)   #user.following.all() #user.profile_set.all()
    activation_key  = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    timestap        = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects         = ProfileManager()

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        print('activation')
        # if self.activated:
        #     pass
        # else:
        #     self.activation_key = 'somekey'  #generate key
        #     self.save()
        #     sent_email = False #send_email()
        #     return sent_email
        if not self.activated:
             self.activation_key = code_generator()  #generate key
             self.save()
             # path_ = reverse  # have to have a url to handle this code on the view.py and the url.py
             path_ = reverse('activate', kwargs={'code':self.activation_key})
             # print(kwargs)
             subject = 'Activate Account'   #get this code https://www.codingforentrepreneurs.com/blog/testing-email-in-django-with-send-mail/
             from_email = settings.DEFAULT_FROM_EMAIL
             # message = f'Activate your account here: {self.activation_key}'
             message = f'Activate your account here: {path_}'
             recipient_list = [self.user.email]
             # html_message = f'<p>Activate your account here: {self.activation_key}</p>'
             html_message = f'<p>Activate your account here: {path_}</p>'
             print(html_message)
             # sent_email = send_mail(
             #                subject,
             #                message,
             #                from_email,
             #                recipient_list,
             #                fail_silently=False,
             #                html_message=html_message)
             sent_email = False
             return sent_email


def post_save_user_reciever(sender, instance, created, *args ,**kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        # default_user_profile = Profile.objects.get(user__id=1)  #user_username__iexact="someone"
        default_user_profile = Profile.objects.get_or_create(user__id=1)[0]    ##this two add follower from the new create user  to existing  members
        default_user_profile.followers.add(instance)
        # default_user_profile.followers.remove(instance)
        # default_user_profile.save()
        profile.followers.add(default_user_profile.user)  ##this two add follower from the members to a new created user
        profile.followers.add(2)

post_save.connect(post_save_user_reciever, sender=User)
