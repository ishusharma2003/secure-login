from django.db import models

class googleformdata(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.first_name} - {self.email} - {self.password}"
     