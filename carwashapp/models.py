from django.db import models
from django.core import validators
# from geopy.point import Point
# from django.contrib.gis.db import models

class Washer_Profile(models.Model):
    washer_name = models.CharField(max_length=200,null=True, blank=False)
    washer_location = models.CharField(max_length=255,null=True, blank=False)
    long_w = models.DecimalField(max_digits=10, decimal_places=2)
    lat_w = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    washer_created = models.DateTimeField(auto_now_add=True)
    
    # def save(self, *args, **kwargs):
    #     self.washer_location = Point(self.long_w, self.lat_w)
    #     super(Washer_Profile, self).save(*args, **kwargs)  

    def __str__(self):
        return f"Washer Name: {self.washer_name}, Status: {self.is_available}"


class Washing_Order(models.Model):
    customer_name  = models.CharField(max_length=255,null=True, blank=False)
    car_model = models.CharField(max_length=255,null=True, blank=False)
    customer_location = models.CharField(max_length=255,null=True, blank=False)
    long_c = models.DecimalField(max_digits=10, decimal_places=2)
    lat_c = models.DecimalField(max_digits=10, decimal_places=2)
    assigned_to = models.ForeignKey(Washer_Profile,on_delete=models.CASCADE, related_name='washingorder',null=True, blank=False)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    order_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer Name: {self.customer_name}"
