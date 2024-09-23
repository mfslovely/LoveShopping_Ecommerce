from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced,SaleProduct
from .forms import CustomerRegistrationform,CustomerProfileForm,ProductForm
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
from datetime import date
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegistrationform,LoginForm
from django.contrib.auth import login,authenticate


class ProductView(View):
    def get(self, request):
        sale_start_date = date(2024, 9, 20)
        sale_end_date = date(2024, 10, 1)
        current_date = date.today()

        is_sale_live = sale_start_date <= current_date <= sale_end_date

        products = Product.objects.all()
        topwears = products.filter(category='TW')
        bottomwears = products.filter(category='BW')
        mobiles = products.filter(category='M')
        laptops = products.filter(category='L')
        frigidger = products.filter(category='RE')
        LivingRoom = products.filter(category='LR')
        skincare= products.filter(category='SK')
        makeup = products.filter(category='Mk')
        haircare = products.filter(category='HC')
        washing = products.filter(category='WM')
        air = products.filter(category='AC')
        fragrances = products.filter(category='FR')

        context = {
            'topwears': topwears,
            'bottomwears': bottomwears,
            'mobiles': mobiles,
            'laptops': laptops,
            'frigidger': frigidger,
            'LivingRoom': LivingRoom,
            'skincare':skincare,
            'makeup':makeup,
            'haircare':haircare,
            'washing':washing,
            'air':air,
            'fragrances':fragrances,           
            'is_sale_live': is_sale_live,
            'is_sale_live': True,
        
        }

        return render(request, 'app/home.html', context)

class SaleProductsView(View):
    def get(self, request):
        current_date = date.today()
        sale_products = SaleProduct.objects.filter(start_date__lte=current_date, end_date__gte=current_date)
        sale_products_ids = sale_products.values_list('product_id', flat=True)
    
        products_on_sale = Product.objects.filter(id__in=sale_products_ids)

        context = {
            'products_on_sale': products_on_sale,
        }

        return render(request, 'app/sale_products.html', context)

class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  return render(request,'app/productdetail.html',{'product':product})

@login_required 
def add_to_cart(request):
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
    messages.success(request, f"{product.title} was added to your cart.")
    return redirect('/cart')

@login_required
def show_cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    if cart_items.exists():
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_details = []

        for item in cart_items:
            product = item.product
            quantity = item.quantity
            tempamount = quantity * product.selling_price
            amount += tempamount
            cart_details.append({
                'product': product,
                'quantity': quantity,
                'tempamount': tempamount
            })

        total_amount = amount + shipping_amount

        return render(request, 'app/addtocart.html', {
            'cart_items': cart_details,
            'totalamount': total_amount,
            'amount': amount
        })
    else:
        return render(request, 'app/emptycart.html')

@login_required
def plus_cart(request):
    prod_id = request.GET.get('prod_id')
    user = request.user
    product = Product.objects.get(id=prod_id)
    
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    cart_item.quantity += 1
    cart_item.save()

    cart_items = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.selling_price for item in cart_items)
    shipping_amount = 70.0

    data = {
        'quantity': cart_item.quantity,
        'amount': amount,
        'totalamount': amount + shipping_amount
    }
    
    return JsonResponse(data)


@login_required
def minus_cart(request):
    prod_id = request.GET.get('prod_id')
    user = request.user
    product = Product.objects.get(id=prod_id)
    
    cart_item = Cart.objects.get(user=user, product=product)
    cart_item.quantity -= 1
    if cart_item.quantity == 0:
        cart_item.delete() 
    else:
        cart_item.save()
    
    cart_items = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.selling_price for item in cart_items)
    shipping_amount = 70.0

    data = {
        'quantity': cart_item.quantity if cart_item.id else 0,
        'amount': amount,
        'totalamount': amount + shipping_amount
    }
    
    return JsonResponse(data)



@login_required
def remove_cart(request):
    prod_id = request.GET.get('prod_id')
    user = request.user
    product = Product.objects.get(id=prod_id)
    
    cart_item = Cart.objects.get(user=user, product=product)
    cart_item.delete()  

    cart_items = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.selling_price for item in cart_items)
    shipping_amount = 70.0

    data = {
        'amount': amount,
        'totalamount': amount + shipping_amount
    }
    
    return JsonResponse(data)


 

def buy_now(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    shipping_amount = 70.0
    totalamount = product.selling_price + shipping_amount

    context = {
        'product': product,
        'add': Customer.objects.filter(user=user),
        'totalamount': totalamount,
    }
    return render(request, 'app/buynow.html', context)



def address(request):
 add = Customer.objects.filter(user = request.user)
 return render(request, 'app/address.html', {'add':add ,'active': 'btn-primary'})

def orders(request):
 op = OrderPlaced.objects.filter(user = request.user)
 return render(request, 'app/orders.html' ,{'order_placed':op})

class CustomerRegistrationView(View):
    user_type = None

    def get(self, request):
        form = CustomerRegistrationform()
        return render(request, 'app/customerregistration.html', {'form': form, 'user_type': self.user_type})

    def post(self, request):
        form = CustomerRegistrationform(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form, 'user_type': self.user_type})

    @classmethod
    def as_view(cls, **initkwargs):
        user_type = initkwargs.pop('user_type', None)
        view = super().as_view(**initkwargs)
        view.user_type = user_type
        return view


class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  return render(request,'app/profile.html',{'form':form, 'active': 'btn-primary'})
 
 def post(self , request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user= usr ,name = name, locality = locality,city = city,state = state,zipcode= zipcode)
   reg.save()
   messages.success(request,'Congratulations !! Profile Updated Succesfully')
  return render (request,'app/profile.html',{'form':form , 'active': 'btn-primary'})
 
def topwears(request, data=None):
    if data is None:
        topwears = Product.objects.filter(category="TW")
    elif data == 'below':
        topwears = Product.objects.filter(category="TW", discounted_price__lt=10000)
    elif data == 'above':
        topwears = Product.objects.filter(category="TW", discounted_price__gt=10000)
    else:
        topwears = Product.objects.filter(category="TW")

    return render(request, 'app/topwears.html', {'topwears': topwears})

def bottomwears(request, data=None):
    if data is None:
        bottomwears = Product.objects.filter(category="BW")
    elif data == 'below':
        bottomwears = Product.objects.filter(category="BW", discounted_price__lt=10000)
    elif data == 'above':
        bottomwears = Product.objects.filter(category="BW", discounted_price__gt=10000)
    else:
        bottomwears = Product.objects.filter(category="BW")

    return render(request, 'app/bottomwears.html', {'bottomwears': bottomwears})

def mobile(request,data=None):
 if data == None:
  mobile = Product.objects.filter(category = "M")
 elif data == 'Redmi' or data == 'Samsung':
  mobile = Product.objects.filter(category = "M").filter(brand = data)
 elif data == 'below':
  mobile = Product.objects.filter(category = "M").filter(discounted_price__lt = 10000)
 elif data == 'above':
  mobile = Product.objects.filter(category = "M").filter(discounted_price__gt = 10000)
 return render(request, 'app/mobile.html',{'mobiles':mobile})


def laptops(request,data=None):
 if data == None:
  laptops = Product.objects.filter(category = "L")
 elif data == 'HP' or data == 'ACER':
  laptops = Product.objects.filter(category = "L").filter(brand = data)
 elif data == 'below':
  laptops = Product.objects.filter(category = "L").filter(discounted_price__lt = 50000)
 elif data == 'above':
  laptops = Product.objects.filter(category = "L").filter(discounted_price__gt = 50000)
 return render(request, 'app/laptops.html',{'laptops':laptops})



def frigidger(request,data=None):
 if data == None:
  frigidger = Product.objects.filter(category = "RE")
 elif data == 'LG' or data == 'Samsung':
  frigidger = Product.objects.filter(category = "RE").filter(brand = data)
 elif data == 'below':
  frigidger = Product.objects.filter(category = "RE").filter(discounted_price__lt = 30000)
 elif data == 'above':
  frigidger = Product.objects.filter(category = "RE").filter(discounted_price__gt = 30000)
 return render(request, 'app/frigidger.html',{'frigidger':frigidger})

def washing(request,data=None):
 if data == None:
  washing = Product.objects.filter(category = "WM")
 elif data == 'LG' or data == 'Samsung':
  washing = Product.objects.filter(category = "WM").filter(brand = data)
 elif data == 'below':
  washing = Product.objects.filter(category = "WM").filter(discounted_price__lt = 30000)
 elif data == 'above':
  washing = Product.objects.filter(category = "WM").filter(discounted_price__gt = 30000)
 return render(request, 'app/washing.html',{'washing':washing})


def air(request,data=None):
 if data == None:
  air = Product.objects.filter(category = "AC")
 elif data == 'Godrej' or data == 'Llyod':
  air = Product.objects.filter(category = "AC").filter(brand = data)
 elif data == 'below':
  air = Product.objects.filter(category = "AC").filter(discounted_price__lt = 30000)
 elif data == 'above':
  air = Product.objects.filter(category = "AC").filter(discounted_price__gt = 30000)
 return render(request, 'app/air.html',{'air':air})

def microwaves(request,data=None):
 if data == None:
  microwaves = Product.objects.filter(category = "M")
 elif data == 'Bosch' or data == 'Samsung':
  microwaves = Product.objects.filter(category = "M").filter(brand = data)
 elif data == 'below':
  microwaves = Product.objects.filter(category = "M").filter(discounted_price__lt = 30000)
 elif data == 'above':
  microwaves = Product.objects.filter(category = "M").filter(discounted_price__gt = 30000)
 return render(request, 'app/microwave.html',{'microwaves':microwaves})

def vacum(request,data=None):
 if data == None:
  vacum = Product.objects.filter(category = "VC")
 elif data == 'Amzon':
  vacum = Product.objects.filter(category = "VC").filter(brand = data)
 elif data == 'below':
  vacum = Product.objects.filter(category = "VC").filter(discounted_price__lt = 3000)
 elif data == 'above':
  vacum = Product.objects.filter(category = "VC").filter(discounted_price__gt = 3000)
 return render(request, 'app/vacum.html',{'vacum':vacum})

def skincare(request,data=None):
 if data == None:
  skincare = Product.objects.filter(category = "SK")
 elif data == 'below':
  skincare = Product.objects.filter(category = "SK").filter(discounted_price__lt = 3000)
 elif data == 'above':
  skincare = Product.objects.filter(category = "SK").filter(discounted_price__gt = 3000)
 return render(request, 'app/skincare.html',{'skincare':skincare})
  
def haircare(request,data=None):
 if data == None:
  haircare = Product.objects.filter(category = "HC")
 elif data == 'below':
  haircare = Product.objects.filter(category = "HC").filter(discounted_price__lt = 3000)
 elif data == 'above':
  haircare = Product.objects.filter(category = "HC").filter(discounted_price__gt = 3000)
 return render(request, 'app/haircare.html',{'haircare':haircare})

def makeup(request,data=None):
 if data == None:
  makeup = Product.objects.filter(category = "Mk")
 elif data == 'below':
  makeup = Product.objects.filter(category = "Mk").filter(discounted_price__lt = 3000)
 elif data == 'above':
  makeup = Product.objects.filter(category = "Mk").filter(discounted_price__gt = 3000)
 return render(request, 'app/makeup.html',{'makeup':makeup})

def fragrances(request,data=None):
 if data == None:
  fragrances = Product.objects.filter(category = "FR")
 elif data == 'below':
  fragrances = Product.objects.filter(category = "FR").filter(discounted_price__lt = 3000)
 elif data == 'above':
  fragrances = Product.objects.filter(category = "FR").filter(discounted_price__gt = 3000)
 return render(request, 'app/fragrances.html',{'fragrances':fragrances})

def exercise(request,data=None):
 if data == None:
  exercise = Product.objects.filter(category = "EX")
 elif data == 'below':
  exercise = Product.objects.filter(category = "EX").filter(discounted_price__lt = 3000)
 elif data == 'above':
  exercise = Product.objects.filter(category = "EX").filter(discounted_price__gt = 3000)
 return render(request, 'app/exercise.html',{'exercise':exercise})

def camping(request,data=None):
 if data == None:
  camping = Product.objects.filter(category = "CG")
 elif data == 'below':
  camping = Product.objects.filter(category = "CG").filter(discounted_price__lt = 3000)
 elif data == 'above':
  camping = Product.objects.filter(category = "CG").filter(discounted_price__gt = 3000)
 return render(request, 'app/camping.html',{'camping':camping})

def sports(request,data=None):
 if data == None:
  sports = Product.objects.filter(category = "SW")
 elif data == 'below':
  sports = Product.objects.filter(category = "SW").filter(discounted_price__lt = 3000)
 elif data == 'above':
  sports = Product.objects.filter(category = "SW").filter(discounted_price__gt = 3000)
 return render(request, 'app/sports.html',{'sports':sports})

def action(request,data=None):
 if data == None:
  action = Product.objects.filter(category = "AF")
 elif data == 'below':
  action = Product.objects.filter(category = "AF").filter(discounted_price__lt = 3000)
 elif data == 'above':
  action = Product.objects.filter(category = "AF").filter(discounted_price__gt = 3000)
 return render(request, 'app/action.html',{'action':action})

def boardGames(request,data=None):
 if data == None:
  boardGames = Product.objects.filter(category = "BG")
 elif data == 'below':
  boardGames = Product.objects.filter(category = "BG").filter(discounted_price__lt = 3000)
 elif data == 'above':
  boardGames = Product.objects.filter(category = "BG").filter(discounted_price__gt = 3000)
 return render(request, 'app/boardGames.html',{'boardGames':boardGames})

def puzzles(request,data=None):
 if data == None:
  puzzles = Product.objects.filter(category = "PU")
 elif data == 'below':
  puzzles = Product.objects.filter(category = "PU").filter(discounted_price__lt = 3000)
 elif data == 'above':
  puzzles = Product.objects.filter(category = "PU").filter(discounted_price__gt = 3000)
 return render(request, 'app/puzzles.html',{'puzzles':puzzles}) 

def EducationalToys(request,data=None):
 if data == None:
  EducationalToys = Product.objects.filter(category = "ET")
 elif data == 'below':
  EducationalToys = Product.objects.filter(category = "ET").filter(discounted_price__lt = 3000)
 elif data == 'above':
  EducationalToys = Product.objects.filter(category = "ET").filter(discounted_price__gt = 3000)
 return render(request, 'app/EducationalToys.html',{'EducationalToys':EducationalToys})

def LivingRoom(request,data=None):
 if data == None:
  LivingRoom = Product.objects.filter(category = "LR")
 elif data == 'below':
  LivingRoom = Product.objects.filter(category = "LR").filter(discounted_price__lt = 3000)
 elif data == 'above':
  LivingRoom = Product.objects.filter(category = "LR").filter(discounted_price__gt = 3000)
 return render(request, 'app/LivingRoom.html',{'LivingRoom':LivingRoom})

client = razorpay.Client(auth=('rzp_test_xPuSwAV5lcswiV', '4CsLam9t070HB3qhVp9RX1b2'))
print(client,"#################################")


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    print(cart_product,"========================")
    
    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.selling_price
            amount += tempamount
        totalamount = amount + shipping_amount

    razorpay_order = client.order.create({
        "amount": int(totalamount * 100),
        "currency": "INR",
        "payment_capture": "1"
    })
    print(razorpay_order["id"],"================")
    context = {
        'add': add,
        'totalamount': totalamount,
        'cart_items': cart_items,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'currency': 'INR',
        'callback_url': 'payment_done', 
        'totalamount_in_paise': int(totalamount * 100)  
    }
    
    return render(request, 'app/checkout.html', context)



# def payment_done(request):
#     if request.method == 'POST':
#         user = request.user
#         custid = request.POST.get('custid')
#         print(f"Customer ID: {custid} received")
        
#         razorpay_payment_id = request.POST.get('razorpay_payment_id')
#         print(f"Razorpay Payment ID: {razorpay_payment_id} received")
        
#         product_id = request.POST.get('product_id')
#         print(f"Product ID: {product_id}")

#         if not custid or not razorpay_payment_id:
#             print("Error: Missing customer ID or payment ID")
#             return JsonResponse({'error': 'Invalid request: Missing customer ID or payment ID'}, status=400)

#         try:
#             customer = Customer.objects.get(id=custid)
#             print(f"Customer found: {customer}")

#             if product_id:
#                 print(f"Processing direct purchase for product ID: {product_id}")
#                 try:
#                     product = Product.objects.get(id=product_id)
#                     OrderPlaced(user=user, customer=customer, product=product, quantity=1).save()
#                     print(f"Order placed for product: {product.title}")
#                 except Product.DoesNotExist:
#                     print(f"Error: Product with ID {product_id} not found")
#                     return JsonResponse({'error': 'Product not found'}, status=404)

#             else:
#                 cart = Cart.objects.filter(user=user)
#                 if not cart.exists():
#                     print("Error: Cart is empty")
#                     return JsonResponse({'error': 'Cart is empty'}, status=400)

#                 for c in cart:
#                     OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
#                     print(f"Order placed for cart item: {c.product.title}")
#                     c.delete()

#             print("Redirecting to orders page")
#             return redirect("orders")

#         except Customer.DoesNotExist:
#             print(f"Error: Customer with ID {custid} not found")
#             return JsonResponse({'error': 'Customer not found'}, status=404)

#     else:
#         print("Error: Invalid request method")
#         return JsonResponse({'error': 'Invalid method: Only POST allowed'}, status=405)



# @csrf_exempt
# def payment_webhook(request):
#     client = razorpay.Client(auth=("rzp_test_xPuSwAV5lcswiV", "4CsLam9t070HB3qhVp9RX1b2"))
#     data = json.loads(request.body)
#     print(data,"=======================")

#     try:
#         client.utility.verify_payment_signature(data)
#         return JsonResponse({'status': 'success'})
#     except razorpay.errors.SignatureVerificationError:
#         return JsonResponse({'status': 'failure'}, status=400)



def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id = custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  print(c,"=======================")
  print(type(c))
  OrderPlaced(user = user,customer=customer,product = c.product, quantity = c.quantity).save()
  c.delete()
 return redirect("orders")


@login_required
def seller_products(request):
    if hasattr(request.user, 'seller'):
        products = Product.objects.filter(seller=request.user.seller)
        return render(request, 'app/seller_products.html', {'products': products})
    else:
        return redirect('home')  # Redirect to home if not a seller

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller  # Ensure seller relationship
            product.save()
            return redirect('seller_products')
    else:
        form = ProductForm()

    return render(request, 'app/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.seller != request.user.seller:  # Ensure the user owns the product
        return HttpResponseForbidden("You are not allowed to edit this product.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'app/edit_product.html', {'form': form})

# class LoginView(View):
#     user_type = None

#     def get(self, request):
#         form = LoginForm()  # Initialize your login form
#         return render(request, 'app/login.html', {'form': form, 'user_type': self.user_type})

#     def post(self, request):
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)  # Log the user in
#                 messages.success(request, 'Login successful!')
                
#                 # Redirect based on user type
#                 if hasattr(user, 'seller'):
#                     return redirect('seller_products')  # Redirect to seller products
#                 else:
#                     return redirect('buyer_home')  # Redirect to buyer home or another page
#             else:
#                 messages.error(request, 'Invalid username or password.')

#         return render(request, 'app/login.html', {'form': form, 'user_type': self.user_type})

#     @classmethod
#     def as_view(cls, **initkwargs):
#         user_type = initkwargs.pop('user_type', None)
#         view = super().as_view(**initkwargs)
#         view.user_type = user_type
#         return view


class SellerLoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_seller:
                return redirect('seller_products')  # Redirect to seller products
            else:
                return redirect('buyer_home')  # Redirect to buyer home
        return render(request, 'app/login.html', {'form': form})

class BuyerLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'app/buyer_login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and not user.is_seller:  # Ensure it's not a seller
                login(request, user)
                return redirect('buyer_home')  # Redirect to buyer home
            else:
                messages.error(request, 'Invalid credentials or not a buyer.')
        return render(request, 'app/buyer_login.html', {'form': form})
    

class CustomLoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                
                # Redirect based on user type
                if user.is_seller:
                    return redirect('seller_products')  # Redirect to seller's product page
                else:
                    return redirect('buyer_home')  # Redirect to buyer's home page
            else:
                messages.error(request, "Invalid username or password")

        return render(request, 'app/login.html', {'form': form})