from django.contrib import admin
from .models import HTTPGETRequest, JSONPOSTRequest

# Register your models here.
admin.site.register(HTTPGETRequest)
admin.site.register(JSONPOSTRequest)