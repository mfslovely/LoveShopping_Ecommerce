from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from mongoengine import Document, fields

# Create your models here.
STATE_CHOICES = (
   ("AN","Andaman and Nicobar Islands"),
   ("AP","Andhra Pradesh"),
   ("AR","Arunachal Pradesh"),
   ("AS","Assam"),
   ("BR","Bihar"),
   ("CG","Chhattisgarh"),
   ("CH","Chandigarh"),
   ("DN","Dadra and Nagar Haveli"),
   ("DD","Daman and Diu"),
   ("DL","Delhi"),
   ("GA","Goa"),
   ("GJ","Gujarat"),
   ("HR","Haryana"),
   ("HP","Himachal Pradesh"),
   ("JK","Jammu and Kashmir"),
   ("JH","Jharkhand"),
   ("KA","Karnataka"),
   ("KL","Kerala"),
   ("LA","Ladakh"),
   ("LD","Lakshadweep"),
   ("MP","Madhya Pradesh"),
   ("MH","Maharashtra"),
   ("MN","Manipur"),
   ("ML","Meghalaya"),
   ("MZ","Mizoram"),
   ("NL","Nagaland"),
   ("OD","Odisha"),
   ("PB","Punjab"),
   ("PY","Pondicherry"),
   ("RJ","Rajasthan"),
   ("SK","Sikkim"),
   ("TN","Tamil Nadu"),
   ("TS","Telangana"),
   ("TR","Tripura"),
   ("UP","Uttar Pradesh"),
   ("UK","Uttarakhand"),
   ("WB","West Bengal")
)


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    name = models.CharField(max_length = 200)
    locality = models.CharField(max_length = 200)
    city = models.CharField(max_length = 50)
    zipcode = models.IntegerField()
    state = models.CharField(choices = STATE_CHOICES ,max_length = 50)

def __str__(self):
    return str(self.id)

CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
    ('RE', 'Refrigerators'),
    ('WM', 'Washing Machines'),
    ('AC', 'Air Conditioners'),
    ('M', 'Microwaves'),
    ('VC', 'Vacuum Cleaners'),
    ('SK', 'Skincare'),
    ('HC', 'Haircare'),
    ('Mk', 'Makeup'),
    ('FR', 'Fragrances'),
    ('EX','Exercise Equipment'),
    ('CG','Camping Gear'),
    ('SW','Sports Wear'),
    ('FC','Fiction'),
    ('NF','Non-Fiction'),
    ('MU','Music'),
    ('MO','Movies'),
    ('AF','Action Figures'),
    ('BG','Board Games'),
    ('PU','Puzzles'),
    ('ET','Educational Toys'),
    ('LR','Living Room'),
    ('BR','Bedroom'),
    ('O','Office'),
    ('S','Storage'),
    ('FP','Fresh Produce'),
    ('BE','Beverages'),
    ('HE','Household Essentials'),
    ('SU','Supplements'),
    ('FE','Fitness Equipment'),
    ('MS','Medical Supplies'),
)


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    seller = models.ForeignKey(Seller,null=True, blank=True, on_delete=models.CASCADE)  # New field for seller
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=200)
    product_image = models.ImageField(upload_to='producting')
    is_sale = models.BooleanField(default=False)
    sale_price = models.FloatField(default=0)

    def discount_percentage(self):
        if self.selling_price and self.discounted_price:
            return int(((self.selling_price - self.discounted_price) / self.selling_price) * 100)
        return 0

    def __str__(self):
        return str(self.title)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    
    def __str__(self):
     return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey (Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    ordered_date = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=50,choices = STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
      return self.quantity * self.product.selling_price
    


class SaleProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # E.g., 15.00 for 15%
    start_date = models.DateField()
    end_date = models.DateField()

   

    def __str__(self):
        return f"{self.product.title} - {self.discount_percentage}% off"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment: {self.user} - {self.amount}"

    
