from django.db import models

# Create your models here.
class JSONPOSTRequest(models.Model):
    # Input Section
    url = models.URLField(max_length=1000)
    headers = models.JSONField()
    sent_data = models.JSONField()
    
    # Output Section.
    received_data = models.JSONField()
    
    def __str__(self):
        return f"JSON POST {self.url}"

class HTTPGETRequest(models.Model):
    # Input Section
    url = models.URLField(max_length=1000)
    headers = models.JSONField()
    # Output Section.
    def __str__(self):
        return f"HTTP GET {self.url}"

