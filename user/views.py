from django.contrib import auth
from django.contrib.auth import login as dj_login,authenticate
from django.core.exceptions import ObjectDoesNotExist, RequestAborted
from django.http import request
from django.http.response import HttpResponse, JsonResponse
import user
from django import forms
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from dashboard.models import cart, productmanagement,usermanagement,cartitem,Otp,delivery
from dashboard.models import Cartadded,cartitem,Ordermanage,Coupon,profile_model,Cartcount
from dashboard.forms import addressform,profile_form,UserForm
import razorpay
from django.views.decorators.csrf import csrf_exempt
from decouple import config






def userpage(request):
    queryset = productmanagement.objects.all()
    qs=0
    if request.session.has_key('username'):
        user = usermanagement.objects.get(UserName=request.session['username'])
        qs = cartitem.objects.filter(user = user).count()
    context = {'products':queryset,'count':qs}
    
    for i in queryset:
        i.final = i.price - (i.price*i.category.discount)/100
    if request.session.has_key('username'):
        
        username = request.session.has_key('username')
     
        return render (request,'userpage/index.html',context)
    else:

        return redirect('userpage2')


def userpage2(request):
    queryset = productmanagement.objects.all()
    context = {'products':queryset}
    for i in queryset:
        i.final = i.price - (i.price*i.category.discount)/100
    return render(request,'userpage/index2.html',context)


def view (request,product_id):
    if request.session.has_key('username'):
        username = request.session.get('username')
        queryset = productmanagement.objects.get(id=product_id)
        user = usermanagement.objects.get(UserName = request.session['username'])
        qs = cartitem.objects.filter(user=user).count()
        
    else:
        return redirect('userpage2')    
    context = {'product':queryset,'username':username,'count':qs}
    return render(request,'userpage/view.html',context)   



def view2 (request,product_id):
    username = request.session.get('username')
    queryset = productmanagement.objects.get(id=product_id)
  
    # user = usermanagement.objects.get(UserName = username)
    context = {'product':queryset,'username':username}
    return render(request,'userpage/view2.html',context)



def signup(request):
    if request.session.has_key('username'):
        return redirect('/')
    else:
        if request.method == 'POST':
            FirstName = request.POST['FirstName']
            UserName  = request.POST['UserName']
            Phone    = request.POST['Phone']
            Email = request.POST['Email']
            Password = request.POST['Password']
            if   usermanagement.objects.filter(UserName=UserName).exists():
                print('user takeny')
                messages.info(request,'UserName Taken')
                return redirect('/')
            elif usermanagement.objects.filter(Phone=Phone).exists():
                print('email phone')
                messages.info(request,'Phone Taken')
                return redirect('/')
            elif usermanagement.objects.filter(Email=Email):
                print('email taken')
                messages.info(request,'Email Taken')
                return redirect('/')
            else:
                print('user craeting')
                user = usermanagement.objects.create(FirstName = FirstName, UserName= UserName, Email=Email, Phone=Phone,Password=Password)
                user.save()
                request.session['username']=UserName
                print('user create')
                return redirect('/')

        else:
            messages.info(request,'Your entered wrong password and username')    
            return render(request,'loginpage/userregister.html')     



def userlogout(request):
    request.session.has_key('Password')
    request.session.flush()
    return redirect('userpage2')



def signin(request):
    if request.method == 'POST':
        UserName = request.POST['UserName']
        Password = request.POST['Password']
        user = usermanagement.objects.filter(UserName=UserName,Password=Password).exists()
        if user:
            user_id = usermanagement.objects.get(UserName=UserName,Password=Password)
            username = usermanagement.objects.get(id=user_id.id)
            if user:
                try:
                    is_exists = cartitem.objects.filter(user=username).exists()
                    if is_exists:
                        cart_item = cartitem.objects.filter(user=username)
                except:
                    pass
            
                request.session['username'] = UserName
                return redirect ('/')  

            else:
                messages.info(request,"somethig went wrong")
                return render(request,'loginpage/userlogin.html') 
        else:
            messages.info(request,'Invalid credentials')
    return render(request,'loginpage/userlogin.html')

#profile details

def profile(request): 
    username = request.session['username']
    user = usermanagement.objects.get(UserName=request.session['username'])
    qs = cartitem.objects.filter(user = user).count()
    user = usermanagement.objects.get(UserName=username)
    try:
        img = profile_model.objects.get(user=user)
    except:
        img = profile_model(user=user)
        img.save()
    form = profile_form(instance=user)
    if request.method == 'POST':
        qs = usermanagement.objects.get(UserName = username)
        form = profile_form(request.POST,request.FILES,instance=img)
        if form.is_valid():
            form.save()
    return render(request,'loginpage/profile.html', {'user':user,'form':form,'img':img,'count':qs})   



def pro_edit(request,id):
    Item = get_object_or_404(usermanagement,id=id)
    if request.method == 'POST':
        forms = UserForm(request.POST,instance=Item)
        if forms.is_valid():
            forms.save()
            print(forms)
            return redirect('profile')
    else:
        forms = UserForm(instance=Item)     
    return render(request,'loginpage/profile_edit.html',{'form':forms})     




# def pro_add(request):
#     if request.method == 'POST':
#         address =  UserForm(request.POST)
#         if address.is_valid():
#             newadd = address.save(commit=False)
#             username = request.session['username']
#             user = usermanagement.objects.get (UserName = username)
#             newadd.user = user
#             newadd.save()
#             return redirect('profile')
#         else:
#             form = UserForm
#             context= {'form':form}
#             return render (request,'loginpage/profile.html',context)    

            
        

# def dp(request):

#     print('helo')
#     if request.method == 'POST':
#         form = profile_model(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#         return redirect('profile')        




  
# ####################################

# order status (my orders)




def my_orders(request,total=0, quantity=0, cart_items=None):   
    username = request.session['username']
    qs = cartitem.objects.all().count()
    try:
        cart = Cartadded.objects.get(cart_id = _cart__id(request)) 
    except:
        messages.info(request,'No orders')
        return render (request,'loginpage/my_order.html')
    cart_items = cartitem.objects.filter(cart=cart, is_active=True)
    user = usermanagement.objects.get(UserName = username)
    querryset= delivery.objects.all().filter(user=user)
    for querry in querryset:
        add =querry
    for cart_item in cart_items:
        if cart_item.product.discount == 0:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        elif request.session.has_key('tot'):
            total = request.session['tot']

        else:
            total += (cart_item.product.last_price() * cart_item.quantity)
            print(total)
    orders = Ordermanage.objects.filter(user=user)
    context = {
        'orders':orders,
        'total' : total,
        'quantity': quantity,
        'user':user,
        'add': add,
        'count':qs
    }
    print(context)
    return render (request,'loginpage/my_order.html',context)    



@csrf_exempt
def my_orderstatus(request):
  
    if request.method == 'POST':
        status1=request.POST['status']
        id=request.POST['id1']
        orders=Ordermanage.objects.get(id=id)
        orders.status=status1
        orders.save()
        return JsonResponse('true',safe=False)
    else:
      
      return redirect('my_orders')

#####################################################

def _cart__id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart




def add_cart(request,product_id):
    # if request.method == 'POST':
    product = productmanagement.objects.get(id=product_id)
    uname = request.session['username']
    user = usermanagement.objects.get(UserName=uname)
    try:
        cart = Cartadded.objects.get(cart_id=_cart__id(request))
    except Cartadded.DoesNotExist:
        cart =  Cartadded.objects.create(
            cart_id = _cart__id(request)

              )   
    cart.save()

    try:
        cart_item = cartitem.objects.get(product=product,cart=cart) ########## 
        cart_item.quantity += 1
        cart_item.save()
    except cartitem.DoesNotExist:
        cart_item = cartitem.objects.create(
            user = user,
            product = product,
            quantity = 1,
            cart = cart,

        )
        cart_item.save()
   
    return redirect('view',product_id)



    
def add_cart2(request,product_id):
    # if request.method == 'POST':
    product = productmanagement.objects.get(id=product_id)
    uname = request.session['username']
    user = usermanagement.objects.get(UserName=uname)
    try:
        cart = Cartadded.objects.get(cart_id=_cart__id(request))
    except Cartadded.DoesNotExist:
        cart =  Cartadded.objects.create(
            cart_id = _cart__id(request)

              )   
    cart.save()

    try:
        cart_item = cartitem.objects.get(product=product,cart=cart) ########## 
        cart_item.quantity += 1
        cart_item.save()
    except cartitem.DoesNotExist:
        cart_item = cartitem.objects.create(
            user = user,
            product = product,
            quantity = 1,
            cart = cart,

        )
        cart_item.save()
   
    return redirect('carthome')




###second cart add in home view#########
def add_cart1(request,product_id):
    # if request.method == 'POST':
    product = productmanagement.objects.get(id=product_id)
    uname = request.session['username']
    user = usermanagement.objects.get(UserName=uname)
    try:
        cart = Cartadded.objects.get(cart_id=_cart__id(request))
    except Cartadded.DoesNotExist:
        cart =  Cartadded.objects.create(
            cart_id = _cart__id(request)
              )   
    cart.save()

    try:
        cart_item = cartitem.objects.get(product=product,cart=cart) ########## 
        cart_item.quantity += 1
        cart_item.save()
    except cartitem.DoesNotExist:
        cart_item = cartitem.objects.create(
            user = user,
            product = product,
            quantity = 1,
            cart = cart,

        )
        cart_item.save()
   
    return redirect('userpage')











def carthome(request,total=0, quantity=0, cart_items=None):
    
    if request.session.has_key('username'):
        try:
            if request.session.has_key('username'):
                user_id = usermanagement.objects.filter(UserName=request.session['username'])
                cart_items = cartitem.objects.filter(user=user_id[0])
                # qs = cartitem.objects.filter(user=user_id).count()
                
                # return render (request,'loginpage/my_order.html')

            cart = Cartadded.objects.get(cart_id = _cart__id(request)) 
            cart_items = cartitem.objects.filter(cart=cart, is_active=True).order_by('id')
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
        except ObjectDoesNotExist:
            pass
          
        context = {
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cart_items,
            
        } 

        return render (request,'userpage/cart.html', context)    

    else:
        return redirect('sighin')





def remove_cart(request,product_id):
    cart = Cartadded.objects.get(cart_id=_cart__id(request))
    product = get_object_or_404(productmanagement,id=product_id)
    cart_item = cartitem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('carthome')    

def remove_cart_item(request,product_id):
    cart = Cartadded.objects.get(cart_id=_cart__id(request))
    product = get_object_or_404(productmanagement,id=product_id)
    cart_item = cartitem.objects.get(product=product,cart=cart)   
    cart_item.delete()
    return redirect('carthome')    


def checkout(request,total=0, quantity=0, cart_items=None):
    try:
        cart = Cartadded.objects.get(cart_id = _cart__id(request)) 
        cart_items = cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.product.discount == 0:     
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            else:    
                total   += (cart_item.product.last_price() * cart_item.quantity)     
         
    except ObjectDoesNotExist:
      pass
    form = addressform()
    username = request.session['username']
    user = usermanagement.objects.get(UserName=username)
    querryset= delivery.objects.all().filter(user=user)
    context = {
        'total' : total,
      
        'cart_items' : cart_items,
        'form' : form,
        'querryset': querryset,
        
    } 
    return render (request,'userpage/checkout.html',context)




def address(request):
    if request.method == 'POST':
        address_form = addressform(request.POST)
        if address_form.is_valid():
            newaddress = address_form.save(commit=False)
            username = request.session['username']
            user = usermanagement.objects.get(UserName=username)
            if request.method == 'POST':
                select = request.POST.get('')
            newaddress.user = user
            newaddress.save()
            
            return redirect('checkout')

        else:
            form =  addressform
            context = {'form':form}
            return render(request,'userpage/checkout.html',context)   
          
           

#####################################checkput delete########
def deladdress(request,id):
    address_id = get_object_or_404(delivery,id=id)
    address_id.delete()  
    return redirect ('checkout')  


def editaddress(request,id):
    Item = get_object_or_404(delivery,id=id)    
    form = addressform(request.POST,instance=Item)
    if form.is_valid():
            form.save()
            return redirect('checkout')
    



    
#####################################################################    




# Otp login


def otplogin(request):
    return render(request,'loginpage/otplogin.html')


def sigh(request):

    if request.method == 'POST':
        num = request.POST['number']
        user = usermanagement.objects.get(Phone = num)
        if user.is_active:
            request.session['firstname'] = user.FirstName
            send = Otp.objects.create(num = num)
            send.save()
            return render(request,'loginpage/otppage.html',{'num':num})
        else:
            messages.error(request,'sorry login again',extra_tags=sigh)
            return redirect('otplogin')
    else:
        return redirect('otplogin')

def verify(request,num):
    if request.method == 'POST':
        otp1=request.POST['otp1']
        otp2=request.POST['otp2']
        otp3=request.POST['otp3']
        otp4=request.POST['otp4']
        otp = otp1+otp2+otp3+otp4
        votp = Otp.objects.get(num = num )
        if votp.checkotp(otp):
            user = usermanagement.objects.get(Phone = num)
            request.session['username']=user.UserName
            votp.delete()
            return redirect('/')
        else:
            return redirect('otplogin')                   


    

# place order (payment section)

def place_order(request, total = 0 , quantity = 0):
    user = usermanagement.objects.get(UserName=request.session['username'])
    qs = cartitem.objects.filter(user = user).count()
    
    if request.session.has_key('username'):
        address_id = request.POST.get('address') 
        request.session['address']=address_id
        # if request.session.has_key('tot'):
        #     total=request.session['tot']
           
            # del request.session['tot']
        delivery_address = delivery.objects.get(id = address_id)    
        cart = Cartadded.objects.get(cart_id = _cart__id(request)) 
        cart_items = cartitem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            if cart_item.product.discount == 0:     
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity

            elif request.session.has_key('tot'):
                total = request.session['tot']


            else:
                for cart_item in cart_items:
                    total   += (cart_item.product.last_price() * cart_item.quantity)
            # request.session['tot'] = total
            request.session['total'] = total
        contex = {'delivery_address' : delivery_address,
                   'total' : total,
                   'quantity': quantity,
                   'count':qs

                  }
        return render (request,'userpage/payment.html',contex)



# payment ##########################################################

def razorpay1(request,total = 0):
    cart= Cartadded.objects.get(cart_id=_cart__id(request))
    cart_items = cartitem.objects.filter(cart=cart,is_active=True)

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        rupee = float(total)*100
        request.session['payment_method']='razorpay'
        order_currency = 'INR'
        key_one = config('key_one')
        key_two = config('key_two')
        client = razorpay.Client(auth=(key_one,key_two))
        payment = client.order.create({'amount': total, 'currency': 'INR',
                                        'payment_capture': '1'}) 
        uname = request.session['username']     

    discount_price = ''                               
    user = usermanagement.objects.get(UserName = uname)
    order=Ordermanage.objects.create(user=user,item=cart_item.product,price=total,status='placed',pay_method='razorpay')
    order.save()
    orde = Ordermanage.objects.get(id=order.id)
    if  request.session.has_key('tot'):
        discount_price=request.session['tot']
        orde.coupon_offer = discount_price
        orde.save() 
        cart_item.delete() 
        del request.session['tot']
        rupee = discount_price
        rupee = float(rupee)*100
        print(rupee)

    contex = {
        'total':total,
        'rupee':rupee,
        'discount_price':discount_price
        
    }        
    
    return render (request,'userpage/razorpay.html',contex)




@csrf_exempt
def success(request,total = 0,quantity=0):
    cart= Cartadded.objects.get(cart_id=_cart__id(request))
    cart_items = cartitem.objects.filter(cart=cart,is_active=True)
    for cart_item in cart_items:
        if request.method == 'POST':
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            uname = request.session['username']
            user = usermanagement.objects.get(UserName = uname)
            
        else:
            return render (request,'userpage/success.html')    
          
    return render (request,'userpage/success.html')





@csrf_exempt
def successp(request,total = 0,quantity=0):
    if request.method == 'POST':

        cart= Cartadded.objects.get(cart_id=_cart__id(request))
        cart_items = cartitem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            if request.method == 'POST':
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
                uname = request.session['username']
                user = usermanagement.objects.get(UserName = uname)
                order = Ordermanage.objects.create(user=user,item=cart_item,price=total,status='placed',pay_method='paypal')   
                order.save()
                cart_item.delete() 

            else:
                return render (request,'userpage/success.html')    
    return render (request,'userpage/success.html')    
         



def cod(request,total = 0,quantity=0):
    address_id = request.session['address']
    address = delivery.objects.get(id=address_id)
    cart= Cartadded.objects.get(cart_id=_cart__id(request))
    cart_items = cartitem.objects.filter(cart=cart,is_active=True)
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    uname = request.session['username']
    user = usermanagement.objects.get(UserName = uname)
    order=Ordermanage()
    order.user = user
    order.item = cart_item.product
    order.price = total
    order.status = 'placed'
    order.address_line2 = "544"
    order.address_line1 = address
    order.save()
    cart_item.delete() 

    if  request.session.has_key('tot'):
        print('hello')
        discount_price=request.session['tot']

        
        order.price = discount_price
        order.save()
        del request.session['tot']
    
    return render (request,'userpage/cod.html')
            
  
    


# paypal
    

def paypal1(request,total=0):
   
    amount = request.session['total']
    request.session['pay_status']='paypal'
    paisa = amount/70
    
    context = {
        'paisa':paisa,
        'total':total
    
    }

    return render(request,'userpage/paypal.html',context)



    
######categories shirts###
def shirt(request):
 
    categories = productmanagement.objects.filter(category = 17)
    catee = productmanagement.objects.all()
    for i in catee:
        i.final = i.price - (i.price*i.category.discount)/100
        i.save()
    return render(request,'userpage/shirt.html',{'categories':categories,'catee':catee})
   

def tshirt(request):
    cat = productmanagement.objects.filter(category = 18)
    catee2 = productmanagement.objects.all()
    for j in catee2:
        j.final = j.price - (j.price*j.category.discount)/100
        j.save()
    
    return render(request,'userpage/TSHIRT.html',{'cat':cat,'catee2':catee2})


####coupon add


def checkcoupon(request,total=0, quantity=0, cart_items=None):
    
    cart = Cartadded.objects.get(cart_id = _cart__id(request)) 
    cart_items = cartitem.objects.filter(cart=cart, is_active=True)
    for cart_item in cart_items:
        total += (cart_item.product.last_price() * cart_item.quantity)
    coupon = request.POST['code']    
    if Coupon.objects.filter(coupon_code = coupon).exists():
        obj = Coupon.objects.get(coupon_code = coupon)
        fre = obj.offer
        x = fre*total/100
        y = total-x
        request.session['tot'] = y
        print(request.session['tot'])
       
        request.session['tot12'] = x
        contex = {
            'total':"%.2f" % x,
            'code':coupon,
            'amount': "%.2f" % y
        }
        return JsonResponse(contex)
    return JsonResponse('false',safe=False)

#######    

    

               


   

        
        
        
           
