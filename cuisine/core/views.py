from django.shortcuts import render, get_object_or_404, reverse,redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Category, Item, Cart, UserDetail,Orders
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import (UserRegisterForm, UpdateUserDetailForm, UserUpdateForm
, UserAddressForm, UserAddressForm1,OrderForm,UserRegisterForms)
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db.models import Q
#from datetime import datetime
#from django.core.mail import EmailMessage
#import random


#------------------------Home Section ------------------------#
def index(request): 
	return render(request, 'core/index.html',{ 'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user])})


#------------------------Account Section ------------------------#
def register(request):  # User Registration
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)
			usr = User.objects.filter(username=username).first()
			usr.save()
			UserDetail(user=usr).save()
			messages.success(request, f'Account is Created for {username}')
			return redirect('login')
		else:
			messages.warning(request, form.errors)
			return redirect('signup')

	form = UserRegisterForm()
	return render(request, 'accounts/signup.html', {'form': form, 'title': 'Sign Up'})


@login_required
def profile(request):  # User profile
	current_user = request.user
	detail = {
		'profile': UserDetail.objects.get(user_id=current_user.id),
	 'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user])
	}
	return render(request, 'accounts/profile.html', detail)


@login_required(login_url='login')  # Check login
def user_update(request):  # User profile edit
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = UpdateUserDetailForm(
			request.POST, request.FILES, instance=request.user.userdetail)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your account has been updated!')
			return HttpResponseRedirect('/profile')
	else:
		user_form = UserUpdateForm(instance=request.user)
		profile_form = UpdateUserDetailForm(instance=request.user.userdetail)
		context = {
			'user_form': user_form,
			'profile_form': profile_form
		}
		return render(request, 'accounts/user_update.html', context)


@login_required(login_url='login')  # Check login
def user_password(request):  # User password change
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(
				request, 'Your password was successfully updated!')
			return HttpResponseRedirect('/profile')
		else:
			messages.error(
				request, 'Please correct the error below.<br>' + str(form.errors))
			return HttpResponseRedirect('/password')
	else:
		form = PasswordChangeForm(request.user)
		return render(request, 'accounts/user_password.html', {'form': form, 
		 'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user])
															   })


#------------------------Category Section ------------------------#
def ItemCategory(request):
	context = {}
	context['cart_element_no'] =len([p for p in Cart.objects.all() if p.user == request.user])

	catg = Category.objects.all().order_by("title")
	context["category"] = catg
	all_items = Item.objects.all().order_by("title")
	context["products"] = all_items
	if "qry" in request.GET: #Searching items
		q = request.GET["qry"]
		# p = request.GET["price"]
		itm = Item.objects.filter(Q(title__icontains=q) | Q(
			category__title__contains=q))
		# itm = add_product.objects.filter(Q(product_name__icontains=q)& Q(sale_price__lt=p))
		# itm = add_product.objects.filter(product_name__contains=q)
		context["products"] = itm
		context["searching"] = "search"
	if "cat" in request.GET:
		cid = request.GET["cat"]
		itm = Item.objects.filter(category__id=cid)
		context["products"] = itm
		context["searching"] = "search"
	return render(request, "core/categories.html", context)


#------------------------Cart and Order ------------------------#
def add_to_cart(request): #Add items to cart
	context = {}
	items = Cart.objects.filter(user__id=request.user.id, status=False)
	context["items"] = items

	if request.user.is_authenticated:
		if request.method == "POST":
			pid = request.POST["pid"]
			qty = request.POST["qty"]
			is_exist = Cart.objects.filter(
				item__id=pid, user__id=request.user.id, status=False)
			if len(is_exist) > 0:
				context["msz"] = "Item Already Exists in Your Cart"
				context["cls"] = "alert alert-warning"
			else:
				product = get_object_or_404(Item, id=pid)
				usr = get_object_or_404(User, id=request.user.id)
				c = Cart(user=usr, item=product, quantity=qty)
				c.save()
				context["msz"] = "{} Added in Your Cart".format(
					product.title)
				context["cls"] = "alert alert-success"
	else:
		context["status"] = "Please Login First to View Your Cart"
		context={ 'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user])}
	return render(request, "core/cart.html", context)


def get_cart_data(request): #Order Summary
	items = Cart.objects.filter(user__id=request.user.id, status=False)
	dilev, total, quantity = 30, 0, 0
	for i in items:
		total += float(i.item.sale_price)*i.quantity
		quantity += int(i.quantity)
		subtotal = total #+ dilev
	res = {
		"total": total, "dilev": dilev, "quan": quantity, 'subtotal':subtotal
	}
	return JsonResponse(res)


def change_quan(request): #Increase and Decrease Quantity
	if "quantity" in request.GET:
		cid = request.GET["cid"]
		qty = request.GET["quantity"]
		cart_obj = get_object_or_404(Cart, id=cid)
		cart_obj.quantity = qty
		cart_obj.save()
		return HttpResponse(cart_obj.quantity)

	if "delete_cart" in request.GET:
		id = request.GET["delete_cart"]
		cart_obj = get_object_or_404(Cart, id=id)
		cart_obj.delete()
		return HttpResponse(1)

#------------------------Order and Payment------------------------#
def orderproduct(request): #Final checkout
	category = Category.objects.all()
	current_user = request.user
	shopcart = Cart.objects.filter(user_id=current_user.id)
	total = 0
	
	for rs in shopcart:
		total += int(rs.item.sale_price) * rs.quantity
		
	if request.method == 'POST':  # if there is a post
		form1 = UserAddressForm1(request.POST)
		form = OrderForm(request.POST)
		#return HttpResponse(request.POST.items())
		if form1.is_valid() and form.is_valid():
			# Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
			# ..............

			data = Orders()
			data.first_name = form1.cleaned_data['first_name'] #get product quantity from form
			data.last_name = form1.cleaned_data['last_name']
			data.address = form.cleaned_data['address']
			data.city = form.cleaned_data['city']
			data.mobile = form.cleaned_data['mobile']
			data.user_id = current_user.id
			data.total = total
			data.ip = request.META.get('REMOTE_ADDR')
			ordercode= get_random_string(5).upper() # random cod
			data.code =  ordercode
			data.save() #


			for rs in shopcart:
				detail = Orders()
				detail.order_id     = data.id # Order Id
				detail.item_id   = rs.item_id
				detail.user_id      = current_user.id
				detail.quantity     = rs.quantity
				detail.sale_price    = rs.item.sale_price
				
				
				detail.save()
				# ***Reduce quantity of sold product from Amount of Product
				#************ <> *****************

			Cart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
			request.session['cart_items']=0
			messages.success(request, "Your Order has been completed. Thank you ")
			return render(request, 'core/Order_Completed.html',{'ordercode':ordercode,'category': category})
		else:
			messages.warning(request, form.errors)
			return HttpResponseRedirect("order")

	form= UserAddressForm1() and UserAddressForm()
	profile = UserDetail.objects.get(user_id=current_user.id)
	context = {'shopcart': shopcart,
			   'category': category,
			   'total': total,
			   'form': form,
			   'profile': profile,
				'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user])
			   }
	return render(request, 'core/checkout.html', context)


def payments(request):
	category = Category.objects.all()
	current_user = request.user
	shopcart = Cart.objects.filter(user_id=current_user.id)
	total = 0
	
	for rs in shopcart:
		total += rs.item.price * rs.quantity    
 

	context = {'title' : 'Payment portal'}
	context['amount_rs'] = total
	context['currency'] = "INR" 
	context['key'] = settings.STRIPE_PUBLISHABLE_KEY
   
	return render(request,'core/payment.html',context)
 
""" 
# Create your views here 
@login_required
def checkout(request):
	if request.method != 'POST':
		messages.error(request,'Please checkout from cart')
		return redirect('cart')    
	
	items = request.session.get('Cart')
	 
	if not items or len(items) <= 0: 
		messages.error(request,'please select atleast one item')
		return redirect('cart')
	
	try:
		with transaction.atomic():
			#print("here 4")
			total_price = getTotalFromOrder(items)
			#print("here 5")
			orderDetails = Order.objects.create(user=request.user,deliveredOn=None,total_price=total_price,offers=discount)

			for item in items:
				menuItem = MenuItem.objects.filter(id=item['id']).first()
				OrderedItem.objects.create(item=menuItem,quantity=item['quantity'],order=orderDetails)
				placedOrdersCount+=1
		#print("here 3")
		tmp = float(request.POST.get('total_amount'))
		total_amount = round(tmp)
		print(total_amount)
		charge = stripe.Charge.create(
			amount=total_amount,
			currency="INR",
			description='A Django charge',
			source=request.POST['stripeToken']
		)
	except Exception as e:
		#print(e)
		placedOrdersCount = 0
		messages.error(request,"cant place order please contact admin")
		return redirect('cart')
	
	request.session['items'] = []

	messages.info(request,'successfully placed '+str(placedOrdersCount)+' order(s)')
	return redirect('home')
 """
#------------------------My order history------------------------#
@login_required(login_url='/login') # Check login
def order_history(request): #My order History
	current_user = request.user
	orders=Orders.objects.filter(user_id=current_user.id)
	context = {
			   'orders': orders,
				'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user])
			   }
	
	return render(request, "core/myorders.html", context)



#------------------------Admin------------------------#
""" Admin Panel """
""" 
def add_product_view(request):
	context = {}
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch) > 0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data
	form = add_product_form()
	if request.method == "POST":
		form = add_product_form(request.POST, request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			login_user = User.objects.get(username=request.user.username)
			data.seller = login_user
			data.save()
			context["status"] = "{} Added Successfully".format(
				data.product_name)

	context["form"] = form

	return render(request, "addproduct.html", context)


def productsList(request):
	context = {}
	ch = register_table.objects.filter(user__id=request.user.id)
	if len(ch) > 0:
		data = register_table.objects.get(user__id=request.user.id)
		context["data"] = data

	all = add_product.objects.filter(
		seller__id=request.user.id).order_by("-id")
	context["products"] = all
	return render(request, "myproducts.html", context)


def update_product(request):
	context = {}
	catg = Category.objects.all().order_by("cat_name")
	context["category"] = catg

	pid = request.GET["pid"]
	product = get_object_or_404(add_product, id=pid)
	context["product"] = product

	if request.method == "POST":
		pn = request.POST["pname"]
		ct_id = request.POST["pcat"]
		pr = request.POST["pp"]
		sp = request.POST["sp"]
		des = request.POST["des"]

		cat_obj = Category.objects.get(id=ct_id)

		product.product_name = pn
		product.product_category = cat_obj
		product.product_price = pr
		product.sale_price = sp
		product.details = des
		if "pimg" in request.FILES:
			img = request.FILES["pimg"]
			product.product_image = img
		product.save()
		context["status"] = "Changes Saved Successfully"
		context["id"] = pid
	return render(request, "update_product.html", context)


def delete_product(request):
	context = {}
	if "pid" in request.GET:
		pid = request.GET["pid"]
		prd = get_object_or_404(add_product, id=pid)
		context["product"] = prd

		if "action" in request.GET:
			prd.delete()
			context["status"] = str(prd.product_name) + \
				" removed Successfully!!!"
	return render(request, "deleteproduct.html", context)

 """