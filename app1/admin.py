from django.contrib import admin
from . models import Registration
from . models import Contact,Cart,Addtoproduct,Order,Booktable

# Register your models here.
admin.site.register(Registration)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Addtoproduct)
admin.site.register(Order)
admin.site.register(Booktable)



