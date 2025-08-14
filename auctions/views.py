from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .models import ListingForm, Listing, UserListing, BiddingForm, CommentForm, Bid, Comment, Watchlist
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from .models import User
from .models import Listing
from .serializers import WatchlistSerializer, RegisterSerializer, LoginSerializer, ListingSerializer, CommentSerializer, UserSerializer, BidSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
import json
import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
    amount=1000, currency='pln', 
    payment_method_types=['card'],
    receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)

def save_stripe_info(request):
    print(request.POST)
    data = request.POST
    email = data['email']
    payment_method_id = data['payment_method_id']
    extra_msg = '' 
    amount = int(request.POST["Highestbid"]) * 100
    customer_data = stripe.Customer.list(email=email).data  
    if len(customer_data) == 0:
    # creating customer
        customer = stripe.Customer.create(
        email=email, payment_method=payment_method_id)
    
    # creating customer
    else:
        customer = customer_data[0]
        extra_msg = "Customer already existed."

    stripe.PaymentIntent.create(
        customer=customer, 
        payment_method=payment_method_id,  
        currency='usd', # you can provide any currency you want
        amount=amount,
        confirm=True)
    id = request.POST["id"]
    product = Listing.objects.get(pk=id)
    product.paid = True
    product.save()
               
     
    return JsonResponse(status=status.HTTP_200_OK, 
      data={
        'message': 'Payment has been done successfully! Artwork Will be delivered in 3 days', 
        'data': {'customer_id': customer.id}   
      })                                     


@method_decorator(csrf_exempt, name='dispatch')
class Register(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):    
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        print(f"{username}, {password}, {email}" )
        confirmPassword = request.data['confirmPassword']
        if password != confirmPassword:
            return Response({"message": "Passwords must match."
            })
        
        try:
            #Unique Email
            if User.objects.filter(email=email).exists():
                return Response({"message":"Email exists"})
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            print("HELLOOOOOOOOOOOO")
            message = {
                            'user': user.username,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        }
            to_email = email
            print("HELLOOOOOOOOOOOO")
            send_mail(mail_subject, json.dumps(message), "artmandi.2021@gmail.com", [to_email])
            print("HELLOOOOOOOOOOOO")            
            
            return HttpResponse('Please confirm your email address to complete the registration')

            #return Response({"message":"Activate your Account"})
        except IntegrityError:
            
            return HttpResponse({"message": "Username already taken."
            })

            
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class= LoginSerializer
    queryset=User.objects.all()    
    permission_classes = [AllowAny]
    @csrf_exempt
    def post(self,request):        
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        print(username,password)
        print(user)
        if user is not None:            
            if user.is_active:
                # print("here")
                
                # token, _ = Token.objects.get_or_create(user=user)
                # print(token)
                # data = {
                #     'Token':token.key
                # }
                login(request, user)
                return Response({"user_id":user.id, "username":username
                }, status=status.HTTP_200_OK)
            return Response({"message": "Not Verified"},status=status.HTTP_400_BAD_REQUEST )
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)


class Logout(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        logout(request)
        return Response({"message": "Logged out"},status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = [IsAuthenticated]
    


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def create(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response( status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):
        serializer.save(created_by= User.objects.get(pk=self.request.data['created_by']))


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['listing']
    
    

    
    def create(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)        
        return Response( status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):
        serializer.save(listing= Listing.objects.get(pk=self.request.data['listing']), 
        user= User.objects.get(pk=self.request.data['user']))


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['listing']
    def create(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        listing = Listing.objects.get(pk= self.request.data['listing'])
        current_bid= int(request.data['bid_price'])
        if current_bid <= listing.start_price:
            return Response({"alert": "Bid must be greater than the current price of Product "})
        all_bids = []
        all_bids = Bid.objects.values("bid_price").filter(listing = self.request.data['listing'])
        max_bid = all_bids.aggregate(Max("bid_price"))
        print(request.user)
        user = User.objects.get(pk = int(request.data['user']))
        watch = Watchlist(listing = listing, user = user)
        if all_bids.count() == 0:
            self.perform_create(serializer)
            watch.save()
            return Response(status=status.HTTP_201_CREATED)
        elif len(all_bids) == 1 and current_bid > max_bid["bid_price__max"]:
            self.perform_create(serializer)
            watch.save()
            return Response(status=status.HTTP_201_CREATED)
        elif len(all_bids) > 1 and current_bid > max_bid["bid_price__max"]:
            self.perform_create(serializer)
            watch.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"alert": "Bid must be greater than Last Bid "}, status=status.HTTP_400_BAD_REQUEST)
        
        if current_bid <= max(all_bids):
            return Response({"alert": "Bid must be greater than the last bid "})

        self.perform_create(serializer)
        watch.save()        
        return Response( status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):
        serializer.save(listing= Listing.objects.get(pk=self.request.data['listing']), 
        user= User.objects.get(pk=self.request.data['user']))


class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


def closebid(request):
    if request.method == "POST":
        listing_id = int(request.POST["listing"])
        all_bids = Bid.objects.filter(listing = listing_id)
        max_bid = all_bids.aggregate(Max("bid_price"))
        bid = Bid.objects.get(bid_price=max_bid["bid_price__max"])
        sold = Listing.objects.get(pk = listing_id)
        sold.bider = bid
        sold.completed = True
        sold.save()
        

        return JsonResponse({"message":"ok"},status=status.HTTP_202_ACCEPTED)
    return HttpResponse({"hi"})

def activate(request):
    token = request.POST["token"]
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(request.POST["uid"]))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
        


    
