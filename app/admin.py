

# Register the models in the campaigns/admin.py file to use Django admin for managing subscribers and campaigns. 
from django.contrib import admin
from .models import Subscriber, Campaign

admin.site.register(Subscriber)
admin.site.register(Campaign)