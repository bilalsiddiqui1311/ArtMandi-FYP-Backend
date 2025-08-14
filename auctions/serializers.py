from .models import Listing, Comment, User, Bid, Watchlist
from rest_framework import serializers
from rest_framework import permissions


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Passwords Must Match',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirmPassword = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Passwords Must Match',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


class LoginSerializer(serializers.ModelSerializer):
     class Meta:
         model=User
         fields=('username','password',) 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]



class ListingSerializer(serializers.ModelSerializer):
    artist =  serializers.CharField( source="created_by.username", read_only=True)
    winner_username = serializers.CharField( source="bider.user.username", read_only=True)
    winner_bidprice = serializers.CharField( source="bider.bid_price", read_only=True)
    
    class Meta:
            PRODUCT_CHOICES = (
            ('E', "ELECTRONICS"),
            ('H', "HOME"),
            ('T', "TOY"),
            ('E', "EDUCATION")        
        )
        
        
            category = serializers.ChoiceField(choices = PRODUCT_CHOICES)
            model = Listing
            fields = ["id",'title', 'description', 'image', 'category', "length" , "width", "paid" , 'start_price', "artist" ,'created_by', "created_at", "end_date", "completed", "winner_username", "winner_bidprice"]
        


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField( source="user.username", read_only=True)
    class Meta:
        model = Comment
        fields = ["listing", "user", 'comment', "username" ]
        
        


class BidSerializer(serializers.ModelSerializer):
    username = serializers.CharField( source="user.username", read_only=True)
    class Meta:
        model = Bid
        fields = ['listing', "user",'bid_price', 'username']
        

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ["listing", "user"]