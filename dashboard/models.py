import user
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Random
from django.db.models.fields import CharField, Field, FloatField
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
import random
from twilio.rest import Client
import datetime, uuid
from decouple import config



# Create your models here.
class categorymanagement(models.Model):
    header_image = models.ImageField(null=True,blank=True,upload_to = "images/")
    category = models.CharField(max_length=255)
    discount = models.IntegerField(default=0)

    def  __str__(self):
        return self.category




class productmanagement(models.Model):
    category = models.ForeignKey(categorymanagement,on_delete=models.CASCADE,null=True)
    product = models.CharField(max_length=255,blank=True)
    brand = models.CharField(max_length=200)
    price = models.FloatField()   
    offerprice = models.IntegerField(default=0) 
    final = models.IntegerField() 
    discount = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    image1 = models.ImageField(null=True,blank=True,upload_to="images/")
    image2 = models.ImageField(null=True,blank=True,upload_to="images/")
    image3 = models.ImageField(null=True,blank=True,upload_to="images/")
    image4 = models.ImageField(null=True,blank=True,upload_to="images/")


    def  __str__(self):
        return  self.product

    def last_price(self):
        if self.discount != 0 or self.category.discount != 0:
            if self.discount > self.category.discount:
                last_price = (self.price * (1 - (self.discount)/100))
                
            else:
                last_price = (self.price * (1 - (self.category.discount)/100))
            return last_price
        return self.price




class usermanagement(models.Model):
    FirstName = models.CharField(max_length=255)
    Email = models.EmailField(max_length=200)
    UserName = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)
    address = models.CharField(max_length=250,blank=True)
    Phone = models.CharField(max_length=200)
    pincode = models.CharField(max_length=200,blank=True)
    dist = models.CharField(max_length=200,blank=True)
    is_active = models.BooleanField(default=True)
     
 
    def  __str__(self):
        return self.FirstName



class Cartcount(models.Model):
    count = models.IntegerField(default=0)
    user = models.ForeignKey(usermanagement,on_delete=CASCADE)




class profile_model(models.Model):
    user = models.OneToOneField(usermanagement,on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,upload_to="images/")        

    

    


class cart(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id




class Cartadded(models.Model):
   
    cart_id = models.CharField(max_length=50) 
    date_added = models.DateField(auto_now_add=True)   

    def __str__(self):
        return self.cart_id    



class cartitem(models.Model):
    user = models.ForeignKey(usermanagement,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(productmanagement,on_delete=models.CASCADE) 
    cart = models.ForeignKey(Cartadded,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity





    # def __str__(self):
    #     return self.product   

class delivery(models.Model):
    user = models.ForeignKey(usermanagement,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    address1=models.CharField(max_length=210)
    address2 = models.CharField(max_length=210)    
    phone = models.FloatField(max_length=30)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=120)
    country = models.CharField(max_length=120)    

    def __str__(self):
        return self.firstname

    




class Otp(models.Model):
    num = models.CharField(max_length=11)
    validnum = random.randint(1000,9999)
    vnum = validnum
    def __str__(self):
        return self.num

    def save(self,*args,**kwargs):
        if self.num is not None:
            account_sid = config('account_sid')
            auth_token = config('auth_token')
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                        body=f'OTP for login  - {self.validnum}',
                                        from_='+1 781 661 5892',
                                        to='+91' +  self.num 
                                    )

            print(message.sid)
        return super().save(*args,**kwargs)  


    def checkotp(self,otp):
        if str(self.vnum) == otp:
            return True
        else:
            return False      


variation_category_choice = (
    ('size','size')
)                   







class variation(models.Model):
    product = models.ForeignKey(productmanagement,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100)     
    variation_value  = models.CharField(max_length=100)
    is_active       = models.BooleanField(default=True)
    create_date = models.DateField(auto_now=True)

    

    def __str__(self):
        return self.product             



            


class Payment(models.Model):
    user = models.ForeignKey(usermanagement,on_delete=models.CASCADE)
    payment_id  = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = {
        ('placed','placed'),
        ('Canceled','Canceled'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
    } 
    PAY_STATUS = {
         ('SUCCESS','SUCCESS'),
          ('FAILURE','FAILURE'),
           ('PENDING','PENDING'),

    }   
    user = models.ForeignKey(usermanagement,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line1 = models.ForeignKey(delivery,on_delete=models.SET_NULL,null=True)
    address_line2 = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return  self.first_name





class Ordermanage(models.Model):
    STATUS = (
        ('Placed','Placed'),
        ('Canceled','Canceled'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),

    )
    PAY_STATUS = (
        ('SUCCESS','SUCCESS'),
        ('FAILURE','FAILURE'),
        ('PENDING','PENDING')
    )
    user = models.ForeignKey(usermanagement,on_delete=models.SET_NULL,null=True)
    item = models.ForeignKey(productmanagement,on_delete=CASCADE)
    order_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    price = models.IntegerField()
    address_line1 = models.ForeignKey(delivery,on_delete=models.SET_NULL,null=True)
    address_line2 = models.CharField(max_length=15)
    status = models.CharField(max_length=40,choices=STATUS,default='PLACED')
    pay_status = models.CharField(choices = PAY_STATUS, max_length=10, default='SUCCESS')
    pay_method = models.CharField(max_length=100,default='COD')
    coupon_offer = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    



###########coupon####
class Coupon(models.Model):
    offer = models.IntegerField(default= 0)
    coupon_code = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)
    
# Create your models here.
