import factory 

from .models import Product 

 

class ProductFactory(factory.django.DjangoModelFactory): 

    class Meta: 

        model = Product 

    tittle = factory.Faker('company')
    
    provider = factory.Faker('company') 
    
    category = factory.Faker('company')
    
    keyword = factory.Faker('company') 
    
    price = factory.Faker('random_int', min=300000, max=9000000) 
    
    stock = factory.Faker('random_int', min=20, max=500) 
    
    description = factory.Faker('company')
    
    
    
    