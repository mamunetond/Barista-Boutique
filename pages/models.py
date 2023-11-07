from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
  tittle = models.CharField(max_length=255)
  provider = models.CharField(max_length=255)
  category = models.CharField(max_length=255)
  keyword = models.CharField(max_length=255)
  image = models.ImageField(upload_to='development', null=True, blank=True)
  price = models.IntegerField()
  stock = models.IntegerField()
  description = models.CharField(max_length=1200)
  created_at_product = models.DateTimeField(auto_now=True)
  updated_at_product = models.DateTimeField(auto_now=True)
  url = models.URLField(blank=True)

class Review(models.Model):
  text = models.CharField(max_length=100)
  date = models.DateTimeField(auto_now_add=True, blank=True)
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  buyAgain = models.BooleanField()
  
  def __str__(self):
      return self.text
    
class Technique(models.Model):
  title = models.TextField()
  author = models.TextField()
  category = models.TextField()
  keyword = models.TextField()
  image = models.ImageField(upload_to='development', null=True, blank=True)
  description = models.TextField()
  product_list = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.title
