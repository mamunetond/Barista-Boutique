from django.db import models


class Product(models.Model):
  tittle = models.CharField(max_length=255)
  provider = models.CharField(max_length=255)
  category = models.CharField(max_length=255)
  keyword = models.CharField(max_length=255)
  price = models.IntegerField()
  stock = models.IntegerField()
  description = models.CharField(max_length=1200)
  created_at_product = models.DateTimeField(auto_now=True)
  updated_at_product = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.tittle
