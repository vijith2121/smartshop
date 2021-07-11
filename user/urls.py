from os import name
from . import views
from django.urls import path


urlpatterns = [
    path('',views.userpage,name='userpage'),
    path('home',views.userpage2,name='userpage2'),
    path('signup',views.signup,name='signup'),
    path('view/<product_id>',views.view,name='view'),
    path('signin/',views.signin,name='sighin'),
    # path('loginpage',views.loginpage,name='loginpage'),
    path('userlogout',views.userlogout,name='userlogout'),
    # path('login',views.loginpage,name='login'),



    path('carthome',views.carthome,name='carthome'),
    path('add_cart/<int:product_id>',views.add_cart,name='add_cart'),
    path('add_cart1/<int:product_id>',views.add_cart1,name='add_cart1'),
    path('add_cart2/<int:product_id>',views.add_cart2,name='add_cart2'),
    # path('cartdel/<int:pk>',views.cartdel,name='cartdel'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item,name='remove_cart_item'),


    path('checkout/',views.checkout,name='checkout'),
    path('address',views.address,name='address'),


    path('otplogin/',views.otplogin,name='otplogin'),
    path('sigh',views.sigh,name='sigh'),
    path('verify/<num>/',views.verify,name='verify'),

    #order (payment section)

    path('place_order', views.place_order,name='place_order'),

    #razorpay
    # path('payment1',views.payment1,name='payment1'),

    path ('razorpay',views.razorpay1,name='razorpay'),
    path('success',views.success,name='success'),

    path('successp',views.successp,name='successp'),

    #####################

    #paypal
    path('paypal',views.paypal1,name='paypal1'),

    #cash on delivery
    path('COD',views.cod,name='COD'),

  

    #delete address
    path('deladdress/<id>/',views.deladdress,name='deladdress'),
    path('editaddress/<id>/',views.editaddress,name='editaddress'),


    
    path('profile/',views.profile,name='profile'),
     path('pro_edit/<int:id>/',views.pro_edit,name='pro_edit'),
     path('pro_add',views.pro_add,name='pro_add'),
    # path('pro',views.pro,name='pro'),
#    path('dp',views.dp,name='dp'),

#order ststus

    path('my_orders',views.my_orders,name='my_orders'),
    path('my_orderstatus',views.my_orderstatus,name='my_orderstatus'),

########categories##
    path('shirt/',views.shirt,name='shirt'),
    path('tshirt/',views.tshirt,name='tshirt'),

    path('checkcoupon',views.checkcoupon,name='checkcoupon'),
  

    
]