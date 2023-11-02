from tkinter import messagebox

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
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
from django.utils.translation import gettext as _


from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings


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
        viewData["products"] = Product.objects.filter(tittle__icontains=search_query)
    else:
        viewData["products"] = Product.objects.all()

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

    viewData['tittle'] = product.tittle + ' - Tienda de Café - El barista' 

    viewData['subtitle'] =  product.tittle + ' - Product information' 

    viewData['product'] = product

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

  def clean_price(self): 
    price = self.cleaned_data.get('price') 

    if price is not None and price <= 0: 
      raise ValidationError('Price must be greater than zero.') 

    return price 

class ProductCreateView(View): 
  template_name = 'products/create.html' 

  def get(self, request): 
    form = ProductForm() 

    viewData = {} 
    viewData['title'] = 'Create product' 
    viewData['form'] = form 

    return render(request, self.template_name, viewData) 

  def post(self, request): 
    form = ProductForm(request.POST) 

    if form.is_valid(): 
      messagebox.showinfo(message='Elemento creado satisfactoriamente')
      form.save() 
      return redirect('index')  

    else: 
      viewData = {} 
      viewData['title'] = 'Create product' 
      viewData['form'] = form 

      return render(request, self.template_name, viewData)
             
class ProductDeleteView(View):
    
    template_name = 'products/delete.html'
    
    def get(self, request, id):
        # Check if product id is valid 

        try: 

            product_id = int(id) 

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
            return redirect('detail', newReview.product.id)
        
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
              return redirect('detail', id)
          except ValueError:
              return render(request, 'reviews/update.html',
              {'review': review,'form':form,'error':'Bad data in form'})
              

@login_required
def deleteReview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.product.id)
        
# techniques views
class TechniqueIndexView(View):
  template_name = 'techniques/index.html'

  def get(self, request):
    viewData = {}
    viewData["title"] = "Techniques - Taller 1"
    viewData["subtitle"] =  "List of techniques"
    
    search_query = request.GET.get('searchProduct')
    if search_query:
        viewData["techniques"] = Technique.objects.filter(title__icontains=search_query)
    else:
        viewData["techniques"] = Technique.objects.all()

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
    viewData["title"] = technique.title + " - Taller 1"
    viewData["subtitle"] =  technique.title + " - Technique information"
    viewData["technique"] = technique

    return render(request, self.template_name, viewData)
  
class TechniqueForm(forms.ModelForm):
  class Meta:
    model = Technique
    fields = ['title', 'author', 'category', 'keyword', 'description', 'product_list']

class TechniqueCreateView(View):
  template_name = 'techniques/create.html'

  def get(self, request):
    form = TechniqueForm()
    viewData = {}
    viewData["title"] = "Create technique"
    viewData["form"] = form
    return render(request, self.template_name, viewData)

  def post(self, request):
    form = TechniqueForm(request.POST)
    if form.is_valid(): 
      form.save()
      viewData = {"title": "Create technique", "form": form, "success_message": "Technique created"}
      return render(request, self.template_name, viewData)
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
      if technique_id < 1:
          raise ValueError("Technique id must be 1 or greater")
      technique = get_object_or_404(Technique, pk=technique_id)
    except (ValueError, IndexError):
      return HttpResponseRedirect(reverse('home'))

    technique.delete()
    return redirect('techniques')    
        
      