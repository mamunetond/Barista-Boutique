from django.urls import include, path
from django.contrib import admin 
from . import views
from .views import (
    AboutPageView,
    HomePageView,
    ProductCreateView,
    ProductDeleteView,
    ProductIndexView,
    ProductShowView,
    TechniqueCreateView,
    TechniqueDeleteView,
    TechniqueIndexView,
    TechniqueShowView,
    ExternalApiShowView
)

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about' ),
    path('products/', ProductIndexView.as_view(), name='index'), 
    path('products/create', ProductCreateView.as_view(), name='form'),
    path('products/<str:id>', ProductShowView.as_view(), name='detail'),
    path('products/<str:id>/delete', ProductDeleteView.as_view(), name='delete'), 
    path('accounts/', include('accounts.urls')),
    path('<int:product_id>', views.detail, name='detail'),
    path('<int:product_id>/create', views.createReview,name='createReview'),
    path('review/<int:review_id>', views.updateReview,name='updateReview'),
    path('review/<int:review_id>/delete', views.deleteReview,name='deleteReview'),
    path('techniques/', TechniqueIndexView.as_view(), name='techniques'),
    path('techniques/create', TechniqueCreateView.as_view(), name='newTechnique'),
    path('techniques/<str:id>', TechniqueShowView.as_view(), name='showTechnique'),
    path('techniques/<str:id>/delete', TechniqueDeleteView.as_view(), name='deleteTechnique'),
    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
    path('products_api/', ExternalApiShowView.as_view(), name='products_api'),
]

