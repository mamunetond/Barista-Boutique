from django.urls import include, path

from . import views
from .views import (
    AboutPageView,
    HomePageView,
    ProductCreateView,
    ProductDeleteView,
    ProductIndexView,
    ProductShowView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about' ),
    path('products/', ProductIndexView.as_view(), name='index'), 
    path('products/create', ProductCreateView.as_view(), name='form'),
    path('products/<str:id>', ProductShowView.as_view(), name='detail'),
    path('products/delete/<str:id>', ProductDeleteView.as_view(), name='delete'), 
    path('accounts/', include('accounts.urls')),
    path('<int:product_id>', views.detail, name='detail'),
    path('<int:product_id>/create', views.createReview,name='createReview'),
    path('review/<int:review_id>', views.updateReview,name='updateReview'),
    path('review/<int:review_id>/delete', views.deleteReview,name='deleteReview'),
]

