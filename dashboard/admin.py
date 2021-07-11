from dashboard.views import usermanagement
from django.contrib import admin
from.models import categorymanagement, delivery,productmanagement,usermanagement, variation
from .models import cart,cartitem,Otp,variation,Payment,Order,Ordermanage,Cartadded,profile_model

# Register your models here.


admin.site.register(categorymanagement)
admin.site.register(productmanagement)
admin.site.register(usermanagement)
admin.site.register(cart)
admin.site.register(cartitem)
admin.site.register(Otp)
admin.site.register(variation)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Ordermanage)
admin.site.register(delivery)
admin.site.register(Cartadded)
admin.site.register(profile_model)


