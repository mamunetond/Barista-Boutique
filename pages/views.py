from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
import requests
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,  # here by default 
)
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView

from .forms import ReviewForm
from .models import Product, Review, Technique

from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings

from cloudinary import uploader
import os

from django import forms
import requests

import xlwt
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph

def change_language(request, language_code):
    if language_code in [lang[0] for lang in settings.LANGUAGES]:
      activate(language_code)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


class HomePageView(TemplateView): 
  template_name = 'pages/home.html'
    
class AboutPageView(TemplateView):
  template_name = 'pages/about.html'
  
  def get_context_data(self, **kwargs): 
    context = super().get_context_data(**kwargs) 

    context.update({ 
        'tittle': 'Tienda de Café', 
        'subtitle': '¡Para los verdaderos amantes de Café !', 
        'description': 'Tu café ideal, a un solo clic', 
        'author': 'Developed by: Mario Alejandro Muñetón Durango', 
      }) 

    return context  
    
class ProductIndexView(View):
  template_name = 'products/index.html'

  def get(self, request):
    viewData = {}
    viewData["title"] = "Tienda de Café - El Barista"
    viewData["subtitle"] =  "Productos"
    
    search_query = request.GET.get('searchProduct')
    if search_query:
        print('query')
        products = Product.objects.filter(tittle__icontains=search_query)
        response = []

        for product in products:
          product_with_image = {}
          if product.image:
            result = uploader.upload(product.image,
                                      cloud_name = 'dbyp3pr3d',
                                      api_key = os.environ.get('CLOUDINARY_KEY'),
                                      api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
                                      secure = True,
                                      )
            product.image = result['secure_url']
            product_with_image['product'] = product
            product_with_image['image'] = product.image
            response.append(product_with_image)
          else:
            product_with_image['product'] = product
            response.append(product_with_image)
        viewData["products"] = response
    else:
        products = Product.objects.all()
        response = []
        for product in products:
            product_with_image = {}
            if product.image:
              result = uploader.upload(product.image,
                                        cloud_name = 'dbyp3pr3d',
                                        api_key = os.environ.get('CLOUDINARY_KEY'),
                                        api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
                                        secure = True,
                                        )
              product.image = result['secure_url']
              product_with_image['product'] = product
              product_with_image['image'] = product.image
              response.append(product_with_image)

              print('product.image', product.image)
            else:
              product_with_image['product'] = product
              response.append(product_with_image)
        print('response', response)
        viewData["products"] = response

    return render(request, self.template_name, viewData)

class ProductShowView(View): 
  template_name = 'products/detail.html'
  
  def get(self, request, id): 
    # Check if product id is valid 
    try: 
      product_id = int(id) 
      if product_id < 1: 
        raise ValueError('Product id must be 1 or greater') 

      product = get_object_or_404(Product, pk=product_id) 
    except (ValueError, IndexError): 
      # If the product id is not valid, redirect to the home page 
      return HttpResponseRedirect(reverse('home')) 
    
    viewData = {} 
    product = get_object_or_404(Product, pk=product_id) 
    response = None
    product_with_image = {}

    if product.image:
      result = uploader.upload(product.image,
                              cloud_name = 'dbyp3pr3d',
                              api_key = os.environ.get('CLOUDINARY_KEY'),
                              api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
                              secure = True,
                              )

      product.image = result['secure_url']
      product_with_image['detail'] = product
      product_with_image['image'] = product.image
      response = product_with_image

    else:
      product_with_image['detail'] = product
      response = product_with_image

    viewData['tittle'] = product.tittle + ' - Tienda de Café - El barista' 
    viewData['subtitle'] =  product.tittle + ' - Product information' 
    viewData['product'] = response
    reviews = Review.objects.filter(product=product)
    viewData['reviews'] = reviews 

    return render(request, self.template_name, viewData)
    
class ProductListView(ListView): 
  model = Product 
  template_name = 'product_list.html' 
  context_object_name = 'products'  # This will allow you to loop through 'products' in your template 

  def get_context_data(self, **kwargs): 
    context = super().get_context_data(**kwargs) 
    context['title'] = 'Tienda de Café - El Barista' 
    context['subtitle'] = 'List of products' 

    return context    
    
class ProductForm(forms.ModelForm): 
  class Meta:
    model = Product
    fields = '__all__'

    # Use FileInput widget for image field
    image = forms.ImageField(required=False, widget=forms.FileInput)

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')

        return price
    
  country = forms.CharField(max_length=100)

  def clean_country(self):
        country = self.cleaned_data.get('country')

        # Realiza una solicitud a la API para verificar si el país existe
        api_url = f'https://restcountries.com/v3.1/name/{country}'
        response = requests.get(api_url)

        if response.status_code != 200:
            raise forms.ValidationError('País no válido. Verifique el nombre del país.')

        return country

class ProductCreateView(View):
  template_name = 'products/create.html'

  def get(self, request):
    form = ProductForm()
    viewData = {}
    viewData["title"] = "Create product"
    viewData["form"] = form
    return render(request, self.template_name, viewData)

  def post(self, request):
    form = ProductForm(request.POST, request.FILES)

    if form.is_valid():
      product = form.save(commit=False)

      country = form.cleaned_data.get('country')
      api_url = f'https://restcountries.com/v3.1/name/{country}'
      response = requests.get(api_url)

      if response.status_code != 200:
          viewData = {"title": "Create product", "form": form, "error_message": "País no válido. Verifique el nombre del país."}
          return render(request, self.template_name, viewData)

      # Check if image is provided
      image = request.FILES.get('image')
      if image:
          # result = uploader.upload(image)
          # product.image = result['secure_url']
          pass

      product.save()
      return redirect('index')
      # return None
    else:
      viewData = {}
      viewData['title'] = 'Create product'
      viewData['form'] = form

      return render(request, self.template_name, viewData)
             
class ProductDeleteView(View):
    
    template_name = 'products/delete.html'
    
    def post(self, request, id):
      # Check if product id is valid 
      try: 
          product_id = int(id) 
          print('product_id', product_id)
          if product_id < 1: 
              raise ValueError('Product id must be 1 or greater') 
          product = get_object_or_404(Product, id=product_id) 
      except (ValueError, IndexError): 
          # If the product id is not valid, redirect to the home page 
          return HttpResponseRedirect(reverse('home')) 
      product = get_object_or_404(Product, id=product_id)
      product.delete()
      return redirect('index')
    
def detail(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    reviews = Review.objects.filter(product = product)
    return render(request, 'products/detail.html', {'product':product, 'reviews': reviews})

@login_required    
def createReview(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    if request.method == 'GET':
        return render(request, 'reviews/create.html', {'form':ReviewForm(), 'product':product})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.product = product
            newReview.save()

            print('newReview in product id', newReview.product.id)

            return redirect('/products/{}'.format(product.id))
        
        except ValueError:
          return render(request,'reviews/create.html', {'form':ReviewForm(), 'error':'bad data passed in'})
        
        
@login_required
def updateReview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)
    if request.user == review.user:
      if request.method == 'GET':
          form = ReviewForm(instance=review)
          return render(request, 'reviews/update.html', {'review': review,'form':form})
      else:
          try:
              form = ReviewForm(request.POST, instance=review)
              form.save()
              return redirect('/products/{}'.format(review.product.id))
          except ValueError:
              return render(request, 'reviews/update.html',
              {'review': review,'form':form,'error':'Bad data in form'})
              

@login_required
def deleteReview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('/products/{}'.format(review.product.id))
        
# techniques views
class TechniqueIndexView(View):
  template_name = 'techniques/index.html'

  def get(self, request):
    viewData = {}
    viewData["title"] = "Techniques - Taller 1"
    viewData["subtitle"] =  "List of techniques"
    
    search_query = request.GET.get('searchProduct')
    if search_query:
        techniques  = Technique.objects.filter(title__icontains=search_query)
        response = []

        for technique in techniques:
          technique_with_image = {}
          if technique.image:
            result = uploader.upload(technique.image,
                                      cloud_name = 'dbyp3pr3d',
                                      api_key = os.environ.get('CLOUDINARY_KEY'),
                                      api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
                                      secure = True,
                                      )
            
            technique.image = result['secure_url']
            technique_with_image['technique'] = technique
            technique_with_image['image'] = technique.image
            response.append(technique_with_image)
          else:
            technique_with_image['technique'] = technique
            response.append(technique_with_image)
        viewData["techniques"] = response
    else:
        techniques = Technique.objects.all()
        response = []
        for technique in techniques:
          technique_with_image = {}
          if technique.image:
            result = uploader.upload(technique.image,
                                      cloud_name = 'dbyp3pr3d',
                                      api_key = os.environ.get('CLOUDINARY_KEY'),
                                      api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
                                      secure = True,
                                      )
             
            technique.image = result['secure_url']
            technique_with_image['technique'] = technique
            technique_with_image['image'] = technique.image
            response.append(technique_with_image)
          else:
            technique_with_image['technique'] = technique
            response.append(technique_with_image)
        viewData["techniques"] = response

    return render(request, self.template_name, viewData)
  
class TechniqueShowView(View):
  template_name = 'techniques/show.html'

  def get(self, request, id):
    try:
        technique_id = int(id)
        if technique_id < 1:
            raise ValueError("Technique id must be 1 or greater")
        technique = get_object_or_404(Technique, pk=technique_id)
    except (ValueError, IndexError):
        # If the technique id is not valid, redirect to the home page
        return HttpResponseRedirect(reverse('home'))
    
    viewData = {}
    technique = get_object_or_404(Technique, pk=technique_id)

    response = None
    technique_with_image = {}

    if technique.image:
      result = uploader.upload(technique.image,
                                cloud_name = 'dbyp3pr3d',
                                api_key = os.environ.get('CLOUDINARY_KEY'),
                                api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
                                secure = True,
                                )
      
      technique.image = result['secure_url']
      technique_with_image['detail'] = technique
      technique_with_image['image'] = technique.image
      response = technique_with_image
    else:
      technique_with_image['detail'] = technique
      response = technique_with_image

    viewData["title"] = technique.title + " - Taller 1"
    viewData["subtitle"] =  technique.title + " - Technique information"
    viewData["technique"] = response

    return render(request, self.template_name, viewData)
  
class TechniqueForm(forms.ModelForm):
  class Meta:
    model = Technique
    # fields = ['title', 'author', 'category', 'keyword', 'description', 'product_list']
    fields = '__all__'

    image = forms.ImageField(required=False, widget=forms.FileInput)

class TechniqueCreateView(View):
  template_name = 'techniques/create.html'

  def get(self, request):
    form = TechniqueForm()
    viewData = {}
    viewData["title"] = "Create technique"
    viewData["form"] = form
    return render(request, self.template_name, viewData)

  def post(self, request):
    print('Create technique')
    form = TechniqueForm(request.POST, request.FILES)

    if form.is_valid(): 
      technique = form.save()
      
      technique.save()
      return redirect('techniques')

      # viewData = {"title": "Create technique", "form": form, "success_message": "Technique created"}
      # return render(request, self.template_name, viewData)
    else:
      viewData = {}
      viewData["title"] = "Create technique"
      viewData["form"] = form
      return render(request, self.template_name, viewData)
    
class TechniqueListView(ListView):
  model = Technique
  template_name = 'technique_list.html'
  context_object_name = 'techniques'  

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Techniques - Taller 1'
    context['subtitle'] = 'List of techniques'
    return context
  
class TechniqueDeleteView(View):
  def post(self, request, id):
    try:
      technique_id = int(id)

      print('technique_id', technique_id)

      if technique_id < 1:
          raise ValueError("Technique id must be 1 or greater")
      technique = get_object_or_404(Technique, pk=technique_id)
    except (ValueError, IndexError):
      return HttpResponseRedirect(reverse('home'))

    technique.delete()
    return redirect('techniques')
  
class ExternalApiShowView(View):
  template_name = 'external_api/show.html'
  def get(self,request):
    #products = []
    #pull data from third party rest api
    response = requests.get('http://34.95.42.190:8000/api/products/')
    #convert reponse data into json
    products_api = response.json()
    print(products_api['Products'])
    #for product in products_api:
      #details = {}
    viewData = {}
    viewData["products_api"] = products_api['Products']
   
      
    return render(request, self.template_name, viewData)

    
  
  
def download_products_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Products')

    row_num = 0
    columns = ['ID', 'Title', 'Category', 'Price', 'Provider', 'Stock', 'Description']
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)
    products = Product.objects.all()


    for product in products:
        row_num += 1
        row = [product.id, product.tittle, product.category, product.price, product.provider, product.stock, product.description]
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

    wb.save(response)
    return response


def download_products_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    products = Product.objects.all()

    data = []
    data.append(['ID', 'Title', 'Category', 'Price', 'Provider', 'Stock'])
    for product in products:
        data.append([product.id, product.tittle, product.category, product.price, product.provider, product.stock])

    col_widths = [1 * inch, 2 * inch, 1.5 * inch, 1 * inch, 1.5 * inch, 1 * inch]

    table = Table(data, colWidths=col_widths)

    doc = SimpleDocTemplate(response)
    elements = []
    elements.append(table)
    doc.build(elements)
    return response
        
      