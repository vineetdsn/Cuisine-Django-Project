from django.db import models
from django.contrib.auth.models import User
import datetime
from django.forms import ModelForm, TextInput, Textarea
from PIL import Image
class UserDetail(models.Model):
	GENDER = (("Male",'Male'),("Female",'Female'),("Other",'Other'))
	STATE_CHOICES = (
		("Andaman & Nicobar Islands",'Andaman & Nicobar Islands'),
		("Andhra Pradesh",'Andhra Pradesh'),
		("Arunachal Pradesh",'Arunachal Pradesh'),
		("Assam",'Assam'),
		("Bihar",'Bihar'),
		("Chandigarh",'Chandigarh'),
		("Chhattisgarh",'Chhattisgarh'),
		("Dadra & Nagar Haveli",'Dadra & Nagar Haveli'),
		("Daman and Diu",'Daman and Diu'),
		("Delhi",'Delhi'),
		("Goa",'Goa'),
		("Gujarat",'Gujarat'),
		("Haryana",'Haryana'),
		("Himachal Pradesh",'Himachal Pradesh'),
		("Jammu & Kashmir",'Jammu & Kashmir'),
		("Jharkhand",'Jharkhand'),
		("Karnataka",'Karnataka'),
		("Kerala",'Kerala'),
		("Lakshadweep",'Lakshadweep'),
		("Madhya Pradesh",'Madhya Pradesh'),
		("Maharashtra",'Maharashtra'),
		("Manipur",'Manipur'),
		("Meghalaya",'Meghalaya'),
		("Mizoram",'Mizoram'),
		("Nagaland",'Nagaland'),
		("Odisha",'Odisha'),
		("Puducherry",'Puducherry'),
		("Punjab",'Punjab'),
		("Rajasthan",'Rajasthan'),
		("Sikkim",'Sikkim'),
		("Tamil Nadu",'Tamil Nadu'),
		("Telangana",'Telangana'),
		("Tripura",'Tripura'),
		("Uttarakhand",'Uttarakhand'),
		("Uttar Pradesh",'Uttar Pradesh'),
		("West Bengal",'West Bengal'),
		)
	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
	user_image = models.ImageField(default='default.png',upload_to='user_photos')
	mobile = models.CharField(max_length=10,null=True)
	email= models.EmailField(blank=True,max_length=40)
	address = models.TextField()
	pincode = models.CharField(max_length=6, null=True)
	landmark = models.CharField(max_length=500, null=True, blank=True)
	locality = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
	gender = models.CharField(max_length=6,choices=GENDER, null=True)
		
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.user_image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.user_image.path)


class Category(models.Model):
	title = models.CharField(max_length=250)
	added_on =models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True, blank=True)

	def __str__(self):
		return self.title

class Item(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=100, blank=False, null=False)
	image = models.ImageField(upload_to='items/images',
							  default="default.png", null=True)
	details = models.TextField()
	slug = models.SlugField(blank=True, unique=True)
	price = models.FloatField(default=0.00, blank=True)
	sale_price = models.CharField(max_length=200)
	is_active = models.BooleanField(default=True, blank=True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return self.title

#store temporary cart data
class Cart(models.Model):
	user =models.ForeignKey(User,on_delete = models.CASCADE)
	item = models.ForeignKey(Item,on_delete = models.CASCADE)
	quantity = models.IntegerField()
	status = models.BooleanField(default=False)
	added_on =models.DateTimeField(auto_now_add=True,null=True)
	update_on = models.DateTimeField(auto_now=True,null=True)

	def __str__(self):
		return self.user.username
""" 
class Order(models.Model):
	cust_id = models.ForeignKey(User,on_delete=models.CASCADE,default='')
	cart_ids = models.CharField(max_length=250)
	item_ids = models.CharField(max_length=250)
	invoice_id = models.CharField(max_length=250)
	status = models.BooleanField(default=False)
	processed_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.cust_id.username

 """
 #store order history
class Orders(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False )
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    total = models.FloatField(null=True)
    status=models.CharField(max_length=10,choices=STATUS,default='Delivered')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name