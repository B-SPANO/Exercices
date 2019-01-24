from django.forms import ModelForm, CharField, HiddenInput
from forum.models import Subscription, Topic, Profile


class SubscriptionForm(ModelForm):
    
    topic = CharField(widget=HiddenInput())
    profile = CharField(widget=HiddenInput())
    
    class Meta:
        model = Subscription
        fields = ['value']