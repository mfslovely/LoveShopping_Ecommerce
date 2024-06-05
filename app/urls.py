from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginFrom,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from django.urls.base import reverse_lazy

urlpatterns = [
    # path('', views.home),
    path('',views.ProductView.as_view(),name="home"),
    # path('', include('app.urls')),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-card/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
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
    
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
