from .models import delivery
from django import forms
from django.db.models import fields
from .models import categorymanagement,productmanagement,usermanagement,Coupon,profile_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.forms import forms



class CategoryForm(forms.ModelForm):
    class Meta:
        model = categorymanagement
        fields = ('category','discount')

class ProductForm(forms.ModelForm):
    class Meta:
        model = productmanagement
        fields = '__all__'

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if productmanagement.exclude(pk=self.instance.pk).filter(is_active=True,product = cleaned_data.get('product')).exists():
    #         raise forms.ValidationError(("product already taken"))
    #         return cleaned_data    



class UserForm(forms.ModelForm):
    class Meta:
        model = usermanagement
        fields = ('FirstName','Email','UserName','Phone','address','dist','pincode')






class profile_form(forms.ModelForm):
    class Meta:
        model = profile_model
        fields = ('image',)

        # def save(self):
        #     image = super(profile_form,self).save()
        #     return image


class addressform(forms.ModelForm):
    class Meta:
        model = delivery
        fields = ('firstname','lastname', 'email','address1','address2','phone','city','state','country' )

class couponform(forms.ModelForm):
    class Meta:
        model = Coupon        
        fields = '__all__'




  
