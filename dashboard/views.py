from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import ProductForm,CategoryForm,couponform
from .models import productmanagement,categorymanagement,delivery,Payment
from .models import usermanagement as userside,cartitem,Cartadded,categorymanagement,Order,Ordermanage,Coupon
from django.contrib.auth.models import User
from django.contrib import messages
from user.views import _cart__id, place_order
from django.core.exceptions import ObjectDoesNotExist
from user import views
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def admin_login(request):
    error = False
    if request.session.has_key('password'):
        return redirect('adminpage')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']   
        if username == 'admin' and password == 'admin':
            request.session['password'] = password
            return redirect('adminpage')
        else:
            error = True
            return render(request,'admin_login.html',{'error' : error})    

    return render (request,'admin_login.html')


def admin_home(request):
    if request.session.has_key('password'):
        user_side = userside.objects.all().count()
        # order = Ordermanage.objects.all().count()
        order_placed = Ordermanage.objects.filter(status='placed').count()
        print(type(order_placed))
      
        order_shipped = Ordermanage.objects.filter(status='Shipped').count()
        order_delivery = Ordermanage.objects.filter(status='deliverd').count()
        print(order_delivery)
   
        total_price = Ordermanage.objects.all()
        total = 0
        for o in total_price:
            total += o.price
            
        
        return render(request,'adminpage.html',{'user_side':user_side,'order_placed':order_placed,'order_shipped':order_shipped,'order_delivery':order_delivery,'total':total})
    else:
        return redirect('admin_login')    
########################################################


# ###########   usermanagmnt #################################

def usermanagement(request):
    Item = userside.objects.all()
    context = {'user' : Item}
    
    return render(request,'usermanagement.html',context)    

def user_block(request,id):
    user = userside.objects.get(id=id)
    user.is_active = not(user.is_active)
    user.save()
    return redirect ('usermanagement')
    # if user.is_active:
    #     user.is_active = False
    #     user.save()
    #     messages.info(request,'User is Blocked')
    # else:
    #     user.is_active = True
    #     user.save()
    #     messages.info(request,'User is Unblocked')
    # return redirect('usermanagement')   


#############################################################


#productmanagement 

def product_management(request):
    queryset = productmanagement.objects.all()
    context = {'products':queryset}
    return render (request,'productmanagement.html',context)  

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = ProductForm()
    posts = productmanagement.objects.all().order_by('-date_posted')    
    return render (request,'addproduct.html', {'form' : form , 'posts' : posts})  



    
    # .order_by('-dated_posted')  

def product_create(request):
    # form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('productmanagement/')    

def productedit(request,id):
    Item = get_object_or_404(productmanagement,id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=Item)
        if form.is_valid():
            form.save()
            return redirect('productmanagement')
    else:
        form = ProductForm(instance=Item)        
    # context = {'form' : form ,'Item' : Item}
    return render(request,'productedit.html',{'form' : form})

def productdel(request,id):
    productdelete = get_object_or_404(productmanagement,id=id)   
    productdelete.delete()
    return redirect ('productmanagement') 
#######################################################################

#ctegorymanagement

def category_management(request):
    queryset = categorymanagement.objects.all()
    context = {'categories':queryset}
    return render(request,'categorymanagement.html',context)  

def add_category(request):
    form = CategoryForm()
    return render(request,'add_category.html',{'form':form})  

def insert_category(request):
    if request.method == 'POST':    
        Category = CategoryForm(request.POST)
        if Category.is_valid():
            Category.save()
            return redirect('categorymanagement/')
        else:
            return redirect('categorymanagement')    
            

def categorydel(request,id):
        cat_del = get_object_or_404(categorymanagement,id=id)
        cat_del.delete()
        return redirect('categorymanagement')


def categorydit(request,id):
    Item = get_object_or_404(categorymanagement,id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=Item)
        if form.is_valid():
            form.save()
            return redirect('categorymanagement')  
    else:
        form = CategoryForm(instance=Item)        
    # context = {'form' : form ,'Item' : Item}
    return render(request,'categorydit.html',{'form' : form})              
              
########################################################################         

# ordermanagement
        
def ordermanagement(request,total=0, quantity=0, cart_items=None):

    if request.session.has_key('password'):
        try:
            cart = Cartadded.objects.get(cart_id = _cart__id(request))
        except:
            return render (request,'ordermanagement.html')    

         
        cart_items = cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    
        orders = Ordermanage.objects.all()
        context = {
            'orders':orders,
            'total' : total,
            'quantity': quantity,
        }
    else:
        return redirect('ordermanagement')    
    return render (request,'ordermanagement.html',context)      





@csrf_exempt
def orderstatus(request):
  
    if request.method == 'POST':
        status1=request.POST['status']
        print(status1)
        id=request.POST['id1']
        orders=Ordermanage.objects.get(id=id)
        orders.status=status1
        orders.save()
        return JsonResponse('true',safe=False)
    else:
      return redirect('ordermanagement')

    ###################################################


#offer management

def offermanagement(request):
    return render(request,'offermanagement.html')      

##########################################################


def admin_logout(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            request.session.flush()
            return redirect('admin_login')       
        else:
            return redirect('adminpage')     
    else:
        return redirect('admin_login')     






##########coupon#####

def couponmanagement(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon':coupon
              }
    return render (request,'couponmanagement.html',context)

def addcoupon(request):
    form = couponform()
    return render(request,'addcoupon.html',{'form':form})    

def insertcoupon(request):
    if request.method == 'POST':
        coupon = couponform(request.POST)
        coupon.save()
        return redirect('couponmanagement')

def delcoupon(request,id):
    coupdel = get_object_or_404(Coupon,id=id)
    coupdel.delete()
    return redirect('couponmanagement')


#####################    


def checkcoupon(request,total=0, quantity=0, cart_items=None):
    if request.method == 'POST':
        coupon = request.POST['coupon']
    cart = Cartadded.objects.get(cart_id = _cart__id(request)) 
    cart_items = cartitem.objects.filter(cart=cart, is_active=True)
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        
    if Coupon.objects.filter(coupon_code = coupon).exists():
        fre = Coupon.objects.get(coupon_code = coupon)
       
        coptotal=fre*4/total
        
    return redirect('checkout')

          

###########          

######Report table######
def report(request):
    if request.method == 'POST':
        date_from=request.POST['datefrom']
        date_to=request.POST['dateto']
        order_search=Ordermanage.objects.filter(date__range=[date_from,date_to])
        return render(request,'report.html',{'orders':order_search})
    else:
        orders = Ordermanage.objects.all()
        return render(request,'report.html',{"orders":orders})






    
    


# def report(request,total=0, quantity=0, cart_items=None):
#     if request.method == 'POST':
#         date_from=request.POST['datefrom']
#         date_to=request.POST['dateto']
#         order_search=Ordermanage.objects.filter(date__range=[date_from,date_to])
#         return render(request,'report.html',{'order':order_search})

#     else:

#         cart = Cartadded.objects.get(cart_id = _cart__id(request)) 
#         cart_items = cartitem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity

#         orders = Ordermanage.objects.all()
#         context = {
#         'orders':orders,
#         'total' : total,
#         'quantity': quantity,
#     }

#         return render(request,'report.html',context)   
        








# def report(request,total=0, quantity=0, cart_items=None):
#     if request.session.has_key('password'):
#         cart = Cartadded.objects.get(cart_id = _cart__id(request)) 
#         cart_items = cartitem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
        

#         orders = Ordermanage.objects.all()
#         context = {
#             'orders':orders,
#             'total' : total,
#             'quantity': quantity,
#         }
    
#     return render(request,'report.html',context)




# def report_search(request):
#      if request.method == 'POST':
#           date_from=request.POST['datefrom']
#           date_to=request.POST['dateto']
#           order_search=Ordermanage.objects.filter(date__range=[date_from,date_to])
#           return render(request,'report.html',{'order':order_search})
#      else:
#          order=Ordermanage.objects.all() 
#          return render(request,'report.html',{'order':order})     

