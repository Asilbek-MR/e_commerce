from django.urls import path
from .views import GetPaymentTotalView,ProcessPaymentView,generateTokenView

# app_name='payment'

urlpatterns=[
    path('get-payment-total',GetPaymentTotalView.as_view()),
    path('get-token',generateTokenView.as_view()),
    path('make-payment',ProcessPaymentView.as_view())
]



