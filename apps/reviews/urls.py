from django.urls import path
from .views import *

urlpatterns=[ 
    path('get-reviews/<productId>',GetProductReviewView.as_view()),
    path('get-review/<productId>',GetProductReviewViews.as_view()),
    path('create-review/<productId>',CreateProductReviewView.as_view()),
    path('update-review/<productId>',UpdateProductReviewView.as_view()),
    path('delete-review/<productId>',DeleteProductReviewView.as_view()),
    path('filter-review/<productId>',FilterProductReviewsView.as_view()),
]






