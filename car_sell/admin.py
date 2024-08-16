from django.contrib import admin
from .models import Brand, Car,Comment,PurchaseHistory

admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(Comment)
admin.site.register(PurchaseHistory)
