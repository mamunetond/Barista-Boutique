from django.test import TestCase
from pages.models import Product, Technique

class TestModels(TestCase):
  def setUp(self):
    self.product1 = Product.objects.create(
      tittle = 'product1',
      provider = 'provider1',
      category = 'category1',
      keyword = 'keyword1',
      image = 'image1',
      price = 100,
      stock = 10,
      description = 'description1',
      url = 'url1'
    )

    self.technique1 = Technique.objects.create(
      title = 'title1',
      author = 'author1',
      category = 'category1',
      keyword = 'keyword1',
      image = 'image1',
      description = 'description1',
      product_list = 'product_list1'
    )

  def test_product_is_assigned_title_on_creation(self):
    self.assertEquals(self.product1.tittle, 'product1')

  def test_technique_is_assigned_title_on_creation(self):
    self.assertEquals(self.technique1.title, 'title1')

