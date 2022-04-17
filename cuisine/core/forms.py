from django import forms
from django.forms import ModelForm,TextInput, EmailInput, Select, FileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import UserDetail,Item,Orders

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget= forms.TextInput
                           (attrs={'placeholder':'Username','class':"form-control"}))
    email = forms.EmailField(max_length=40,widget= forms.EmailInput
                           (attrs={'placeholder':'Email','class':"form-control"}))
    first_name = forms.CharField(max_length=100,widget= forms.TextInput
                           (attrs={'placeholder':'First Name','class':"form-control"}))
    last_name = forms.CharField(max_length=100, widget= forms.TextInput
                           (attrs={'placeholder':'Last Name','class':"form-control"}))
    password1 = forms.CharField(max_length=100, widget= forms.PasswordInput
                           (attrs={'placeholder':'Password','class':"form-control"}))
    password2 = forms.CharField(max_length=100, widget= forms.PasswordInput
                           (attrs={'placeholder':'Confirm Password','class':"form-control"}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name' ,'email', 'password1', 'password2']

#Used for reaming profile information 
class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = (
			'first_name',
			 'last_name',
			 'username',
			 'email',
		)
		
#Used for reaming profile information 
class UpdateUserDetailForm(forms.ModelForm):
	class Meta:
		model = UserDetail
		fields = [
			'user_image',
			'mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
			'gender',
		]

#Used in final checkout
class UserAddressForm1(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'first_name',
			 'last_name',
		]

#Used in final checkout		
class UserAddressForm(forms.ModelForm):
	class Meta:
		model = UserDetail
		fields = [
			'mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
		]


class OrderForm(ModelForm):
    class Meta:
        model = UserDetail
        fields = ['address','mobile','city','state','pincode',
			'landmark',
			'locality',
		]
""" 
class add_product_form(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title","category","price","sale_price","image","details"]
 """

 
class UserRegisterForms(PasswordChangeForm):
    old_password = forms.CharField(max_length=30, widget= forms.TextInput
                           (attrs={'placeholder':'old_password','class':"form-control"}))
    new_password1 = forms.CharField(max_length=100, widget= forms.PasswordInput
                           (attrs={'placeholder':'New Password','class':"form-control"}))
    new_password2 = forms.CharField(max_length=100, widget= forms.PasswordInput
                           (attrs={'placeholder':'Confirm Password','class':"form-control"}))
