from django.contrib import admin
from .models import Listing, User, UserListing, Bid, Comment, Watchlist
from django.forms import ModelForm, ValidationError, fields

# class AdminBidForm(ModelForm):
#     class Meta:
#         model = Bid
#         fields = ("listing", "user", "bid_price")

#     def clean(self):
#         l = Listing.objects.get(listing= self.cleaned_data.get('listing'))
#         bid_price = self.cleaned_data.get('bid_price')
#         start_price = self.cleaned_data.get('listing')
#         print(l)
#         # if bid_price <= start_price:
#         #     raise ValidationError("TEST EXCEPTION!")


# class AdminBid(admin.ModelAdmin):
#     form = AdminBidForm

# Register your models here.
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(UserListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
