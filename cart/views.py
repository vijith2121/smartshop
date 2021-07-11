from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login as dj_login,authenticate
import user
from django import forms
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.contrib import messages
from dashboard.models import productmanagement,usermanagement,cart,cartitem
from django.contrib.auth.decorators import login_required



def carthome(request):
    queryset = productmanagement.objects.all()
    context = {'products' : queryset}
    return render(request,'userpage/cart.html',context)  
    