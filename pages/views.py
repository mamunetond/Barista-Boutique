from django.shortcuts import render # here by default 
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

 
# Create your views here. 


class HomePageView(TemplateView): 

    template_name = 'pages/home.html'
    

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs): 

        context = super().get_context_data(**kwargs) 

        context.update({ 

            "title": "Tienda de Café", 

            "subtitle": "¡Para los verdaderos amantes de Café !", 

            "description": "Tu café ideal, a un solo clic", 

            "author": "Developed by: Mario Alejandro Muñetón Durango", 

        }) 

 

        return context
    
    
    
class ProductIndexView(View): 

    template_name = 'products/index.html' 

 

    def get(self, request): 

        viewData = {} 

        viewData["title"] = "Tienda de Café - El Barista" 

        viewData["subtitle"] =  "Productos - Métodos de Filtrado" 

        viewData["products"] = Product.objects.all() 

 

        return render(request, self.template_name, viewData) 

 

class ProductShowView(View): 

    template_name = 'products/show.html'
    
    def get(self, request, id): 
        
        # Check if product id is valid 

        try: 

            product_id = int(id) 

            if product_id < 1: 

                raise ValueError("Product id must be 1 or greater") 

            product = get_object_or_404(Product, pk=product_id) 

        except (ValueError, IndexError): 

            # If the product id is not valid, redirect to the home page 

            return HttpResponseRedirect(reverse('home')) 
        
        viewData = {} 

        product = get_object_or_404(Product, pk=product_id) 

        viewData["title"] = product.tittle + " - Tienda de Café - El barista" 

        viewData["subtitle"] =  product.tittle + " - Product information" 

        viewData["product"] = product 

 

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

        viewData["title"] = "Create product" 

        viewData["form"] = form 

        return render(request, self.template_name, viewData) 

 

    def post(self, request): 

        form = ProductForm(request.POST) 

        if form.is_valid(): 
            messagebox.showinfo(message='Elemento creado satisfactoriamente')
            form.save() 
            return redirect('index')  

        else: 

            viewData = {} 

            viewData["title"] = "Create product" 

            viewData["form"] = form 

            return render(request, self.template_name, viewData)
        
        
class ProductDeleteView(View):
    
    template_name = 'products/delete.html'
    
    def get(self, request, id):
        # Check if product id is valid 

        try: 

            product_id = int(id) 

            if product_id < 1: 

                raise ValueError("Product id must be 1 or greater") 

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
    return render(request, 'detail.html', 
                  {'product':product, 'reviews': reviews})

@login_required    
def createreview(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    if request.method == 'GET':
        return render(request, 'reviews/createreview.html', {'form':ReviewForm(), 'product':product})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.product = product
            newReview.save()
            return redirect('show', newReview.product.id)
        
        except ValueError:
            return render(request,'reviews/createreview.html', {'form':ReviewForm(), 'error':'bad data passed in'})
        
        
@login_required
def updatereview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', 
                      {'review': review,'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', id)
        except ValueError:
            return render(request, 'updatereview.html',
             {'review': review,'form':form,'error':'Bad data in form'})
            

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.product.id)
        
        
        
        
       
       
        
        
        
        
    
       
    
    
    

      
