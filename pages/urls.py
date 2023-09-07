from django.urls import path,include
from .views import HomePageView, AboutPageView, ProductIndexView, ProductCreateView, ProductShowView, ProductDeleteView
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about' ),
    path('products/', ProductIndexView.as_view(), name='index'), 
    path('products/create', ProductCreateView.as_view(), name='form'),
    path('products/<str:id>', ProductShowView.as_view(), name='detail'),
    path('products/delete/<str:id>', ProductDeleteView.as_view(), name='delete'), 
    path('accounts/', include('accounts.urls')),
    path('<int:product_id>', views.detail, name='detail'),
    path('<int:product_id>/create', views.createreview,name='createreview'),
    path('review/<int:review_id>', views.updatereview,name='updatereview'),
    path('review/<int:review_id>/delete', views.deletereview,name='deletereview'),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
