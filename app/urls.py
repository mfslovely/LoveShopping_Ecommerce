from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginFrom,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from django.urls.base import reverse_lazy
from .views import ProductView,SaleProductsView,CustomerRegistrationView,SellerLoginView,BuyerLoginView

urlpatterns = [
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-card/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    # path('buy/', views.buy_now, name='buy-now'),
    path('buy/<int:product_id>/', views.buy_now, name='buy_now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('topwears/', views.topwears, name='topwears'),
    path('topwears/<str:data>/', views.topwears, name='topwears_filter'),  # Topwears view
    path('bottomwears/', views.bottomwears, name='bottomwears'),
    path('bottomwears/<str:data>/', views.bottomwears, name='bottomwears_filter'),  # Bottomwears view
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('accounts/login',auth_views.LoginView.as_view(template_name= 'app/login.html',authentication_form = LoginFrom), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page = 'login'),name= 'logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name = 'app/passwordchange.html', form_class = MyPasswordChangeForm,success_url='/passwordchangedone/'),name= 'passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name = 'app/passwordchangedone.html'),name= 'passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name = 'app/password_reset.html',form_class = MyPasswordResetForm),name = 'password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'),name = 'password_reset_done'),
    
    path('password-reset-confrim/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html ' , success_url=reverse_lazy('password_reset_complete') , form_class = MySetPasswordForm),name = 'password_reset_confrim'),   
   
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'),name = 'password_reset_complete'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('seller_registration/', CustomerRegistrationView.as_view(user_type='seller'), name='seller_registration'),
    path('buyer_registration/', CustomerRegistrationView.as_view(user_type='buyer'), name='customerregistration'),
    path('laptop/', views.laptops, name='laptop'),
    path('laptop/<slug:data>', views.laptops, name='laptopdata'),
    path('frigidger/',views.frigidger,name='frigidger'),
    path('frigidger/<slug:data>',views.frigidger,name='frigidger'),
    path('washing/',views.washing,name='washing'),
    path('washing/<slug:data>',views.washing,name='washing'),
    path('air/',views.air,name='air'),
    path('air/<slug:data>',views.air,name='air'),
    path('microwaves/',views.microwaves,name='microwaves'),
    path('microwaves/<slug:data>',views.microwaves,name='microwaves'),
    path('vacum/',views.vacum,name='vacum'),
    path('vacum/<slug:data>',views.vacum,name='vacum'),
    path('skincare/',views.skincare,name='skincare'),
    path('skincare/<slug:data>',views.skincare,name='skincare'),
    path('haircare/',views.haircare,name='haircare'),
    path('haircare/<slug:data>',views.haircare,name='haircare'),
    path('makeup/',views.makeup,name='makeup'),
    path('makeup/<slug:data>',views.makeup,name='makeup'),
    path('fragrances/',views.fragrances,name='fragrances'),
    path('fragrances/<slug:data>',views.fragrances,name='fragrances'),
    path('exercise/',views.exercise,name='exercise'),
    path('exercise/<slug:data>',views.exercise,name='exercise'),
    path('camping/',views.camping,name='camping'),
    path('camping/<slug:data>',views.camping,name='camping'),
    path('sports/',views.sports,name='sports'),
    path('sports/<slug:data>',views.sports,name='sports'),
    path('action/',views.action,name='action'),
    path('action/<slug:data>',views.action,name='action'),
    path('boardGames/',views.boardGames,name='boardGames'),
    path('boardGames/<slug:data>',views.boardGames,name='boardGames'),
    path('puzzles/',views.puzzles,name='puzzles'),
    path('puzzles/<slug:data>',views.puzzles,name='puzzles'),
    path('EducationalToys/',views.EducationalToys,name='EducationalToys'),
    path('EducationalToys/<slug:data>',views.EducationalToys,name='EducationalToys'),
    path('LivingRoom/',views.LivingRoom,name='LivingRoom'),
    path('LivingRoom/<slug:data>',views.LivingRoom,name='LivingRoom'),
    path('sale-products/', SaleProductsView.as_view(), name='on_sale_products'),
    path('payment_done/', views.payment_done, name='payment_done'),
    # path('payment/webhook/', views.payment_webhook, name='razorpay_webhook'),
    path('seller/products/', views.seller_products, name='seller_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller/login/', SellerLoginView.as_view(), name='seller_login'),
    path('buyer/login/', BuyerLoginView.as_view(), name='buyer_login'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
