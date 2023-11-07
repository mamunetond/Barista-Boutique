from django.contrib import admin 
from django.urls import path,include
from rest_framework.documentation import include_docs_urls

 

urlpatterns = [ 
    path('admin/', admin.site.urls, name='administration'), 
    path('', include('pages.urls')),
    path('api_Product/', include('api_Product.urls')),
    path('docs_Product/', include_docs_urls(title = 'Api Product Barista Boutique Documentation')),
] 
