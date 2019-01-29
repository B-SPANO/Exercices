from django.forms import ModelForm, CharField, HiddenInput
from forum.models import Subscription, Topic, Profile


class SubscriptionForm(ModelForm):
    """
    Define specific hidden field for form
    """

    topic = CharField(widget=HiddenInput())
    profile = CharField(widget=HiddenInput())

    class Meta:
        """ Define model form used  """
        model = Subscription
        fields = ['value']
