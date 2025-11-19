from django.urls import path
from store.views import Index, Signup, Login, logout, Cart, CheckOut, OrderView

from django.contrib import admin
from django.urls import path
from store.views import CustomAdminLoginView

admin.site.site_header = 'E-Shop Store admin'
admin.site.site_title = 'E-Shop Store admin'
admin.site.index_title = 'E-Shop Store administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/login/', CustomAdminLoginView.as_view(), name='admin_login'),
    path('', Index.as_view(), name='homepage'),
    path('homepage/', Index.as_view(), name='homepage'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart/', Cart.as_view(), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'),
]