from django.db import models
from apps.product.models import Product
from datetime import datetime
from django.conf import settings
User=settings.AUTH_USER_MODEL

class Review(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rating=models.DecimalField(max_digits=2,decimal_places=1)
    comment=models.TextField()
    date_created=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.comment


















