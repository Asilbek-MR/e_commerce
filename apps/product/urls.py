from django.urls import path
from .views import productDetailView,ListBySearchView,ListProductView,ListRelatedView,ListSearchView

# app_name='product'
urlpatterns=[
    path('product/<productId>',productDetailView.as_view()),
    path('get-products',ListProductView.as_view()),
    path('search',ListBySearchView.as_view()),
    path('related/<productId>',ListRelatedView.as_view()),
    path('by/search',ListBySearchView.as_view()),
]




