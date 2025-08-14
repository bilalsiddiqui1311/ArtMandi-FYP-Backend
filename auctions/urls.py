from django.urls import path
from . import views

from django.urls import include, path
from rest_framework import routers
from .views import LoginView, Logout, Register


router = routers.DefaultRouter()
router.register(r"User", views.UserViewSet)
router.register(r"Comment", views.CommentViewSet, basename='Comments')
router.register(r'Listing', views.ListingViewSet)
router.register(r'Bid', views.BidViewSet)
router.register(r'Watchlist', views.WatchlistViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),
    path("closebid/", views.closebid, name="closebid"),
    path("login/", LoginView.as_view()),
    path("logout/", Logout.as_view(), name="logout"),
    path("register/", Register.as_view(), name="register"),
    path("test-payment/", views.test_payment),
    path("save-stripe-info/", views.save_stripe_info),
    path("activate/", views.activate),
    
    
    #path("listing", views.create_listing, name= "listing"),
    #path("product/<int:product_id>/<int:user_id>", views.product, name="product"),
    #path("CloseBid/<int:product_id>", views.product, name = "CloseBid")
]


