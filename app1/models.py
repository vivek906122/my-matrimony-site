from django.db import models

# Create your models here.

class Registration(models.Model):
    regi_name  = models.TextField(max_length=250)
    regi_email = models.EmailField(max_length=250)
    regi_psw = models.TextField(max_length=250)
    regi_img = models.FileField(upload_to='profile_images',null=True)

    def __str__(self) -> str:
        return self.regi_name
    
class Contact(models.Model):
    con_name = models.TextField(max_length=250)
    con_email = models.EmailField(max_length=250)
    con_num = models.CharField(max_length=250)
    con_area = models.TextField()

    def __str__(self) -> str:
        return self.con_name



    
class Addtoproduct(models.Model):
    pro_name = models.CharField(max_length=250)
    pro_price = models.FloatField(max_length=250)
    pro_image = models.FileField(null=True,upload_to="products")
    pro_desc = models.TextField(null=True) 

    def __str__(self) -> str:
        return self.pro_name

class Cart(models.Model):
    cart_user = models.CharField(max_length=250)
    cart_proid = models.IntegerField(null=True)
    cart_name  = models.CharField(max_length=250)
    cart_price = models.FloatField(max_length=250)
    cart_image = models.FileField()
    cart_qty = models.IntegerField()
    cart_amount = models.FloatField()


    def __str__(self) -> str:
        return self.cart_name

class Order(models.Model):
    order_user = models.CharField(max_length=250,default=None,null=True)
    order_name = models.CharField(max_length=250)
    order_price = models.FloatField(max_length=250)
    order_image = models.FileField(null=True)
    order_qty = models.IntegerField()
    order_amount = models.FloatField()
    order_address = models.TextField(null=True)
    order_paytype = models.CharField(max_length=250,null=True)
    order_status = models.IntegerField(default=0)
    checkout_email = models.CharField(max_length=250,null=True)
    checkout_phone = models.CharField(max_length=250,null=True)
    checkout_name = models.CharField(max_length=250,null=True)
    checkout_address = models.TextField(max_length=250,null=True)
    checkout_city = models.TextField(max_length=250,null=True)
    checkout_country = models.TextField(max_length=250,null=True)
    checkout_postal = models.CharField(max_length=255,null=True)


    def __str__(self) -> str:
        return self.order_name


class Booktable(models.Model):
    date = models.DateField()
    time = models.TimeField()
    seats = models.CharField(max_length=15)
    place = models.TextField(max_length=30)
    food = models.TextField(max_length=255)
    user = models.CharField(max_length=255,null=True)

    def __str__(self) -> str:
        return self.date












