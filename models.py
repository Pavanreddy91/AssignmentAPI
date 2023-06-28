from django.db import models

 

class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    user = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    software = models.CharField(max_length=100)
    seats = models.IntegerField()
    amount = models.FloatField()