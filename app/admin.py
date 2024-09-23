from django.contrib import admin
from .models import(
    Customer,
    Product,
    Cart,
    OrderPlaced,SaleProduct,Payment,Seller
)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status']

@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'discount_percentage', 'start_date', 'end_date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','order_id','status','created_at','transaction_id']

# @admin.register(Seller)



class SellerAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Customize this to show other fields if you add more
    search_fields = ('user__username',)  # Allows searching by username

admin.site.register(Seller, SellerAdmin)