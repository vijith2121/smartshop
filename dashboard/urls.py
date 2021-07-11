from os import name
from . import views
from django.urls import path


urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('adminpage',views.admin_home,name='adminpage'),
    path('adminlogout',views.admin_logout,name='adminlogout'),


    path('usermanagement',views.usermanagement,name='usermanagement'),
    path('user_block/<int:id>/',views.user_block,name='user_block'),



    path('productmanagement/',views.product_management,name='productmanagement'),
    path('add_product',views.add_product,name='add_product'),
    path('product_create',views.product_create,name='product_create'),
    path('productedit/<int:id>',views.productedit,name='productedit'),
    path('productdel/<int:id>',views.productdel,name='productdel'),
    


    path('categorymanagement/',views.category_management,name='categorymanagement'),
    path('add_category',views.add_category,name='add_category'),
    path('insert_category',views.insert_category,name='insert_category'),
    path('categorydel/<int:id>',views.categorydel,name='categorydel'),
    path('categorydit/<int:id>/',views.categorydit,name='categorydit'),

   
    path('offermanagement',views.offermanagement,name='offermanagement'),

    path('ordermanagement',views.ordermanagement,name='ordermanagement'),

    path('orderstatus/',views.orderstatus,name='orderstatus'),

    #####coupon 
    path('couponmanagement/',views.couponmanagement,name='couponmanagement'),
    path('addcoupon',views.addcoupon,name='addcoupon'),
    path('insertcoupon',views.insertcoupon,name='insertcoupon'),
    path('delcoupon/<int:id>/',views.delcoupon,name='delcoupon'),

    ####report#####
    path('report',views.report,name='report'),
   
]