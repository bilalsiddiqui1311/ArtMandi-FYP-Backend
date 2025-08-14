def index(request):
    products = Listing.objects.all()
    return render(request, "auctions/index0.html",{
        'products': products
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    form = ListingForm()
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid:
            form.save(commit=False)            
            title = request.POST["title"]
            description = request.POST["description"]
            image = request.POST["image"]
            category = request.POST["category"]
            start_price = request.POST["start_price"]
            listing = Listing( title=title, description= description, image= image,category= category, start_price= start_price)
            listing.save()
            user_listing = UserListing(user=request.user, Listing=listing)
            user_listing.save()     
        return render(request, "auctions/listing.html",{
            "message": "Product added Successffully"
        })
    else:
        return render(request, "auctions/listing.html",{
            "form":form
        }
        )

@login_required
def product(request, product_id, user_id):
    user_listing = UserListing.objects.get(Listing=product_id)
    product = Listing.objects.get(pk=product_id)
    user_comment = User.objects.get(pk=user_id)
    max_bid = Bid.objects.aggregate(Max("bid_price"))
    bidding = BiddingForm()
    comment = CommentForm()
    if request.method =="POST":
        if "Bid" in request.POST:
            bidding = BiddingForm(request.POST)
            current_bid = int(request.POST["bid_price"])
            
            if bidding.is_valid:
                if current_bid <= product.start_price:
                    return render(request, "auctions/product.html",{
                            "product": product,
                            "bidding": bidding,
                            "user_listing": user_listing,
                            "comments": comment,
                            "Max_Bid": max_bid["bid_price__max"],
                            "error":"Bid needs to be higher than the start price or previous Bid"
                        })

                if current_bid > product.start_price:
                    if Bid.objects.count() == 0:
                        set_bid = Bid(user_listing=user_listing, bid_price=current_bid, user=user_comment)
                        set_bid.save()
                        return HttpResponse("Bid Successful")


                    elif Bid.objects.count() > 0 and current_bid > (max_bid["bid_price__max"]):
                        set_bid = Bid(user_listing=user_listing, bid_price=current_bid, user=user_comment)
                        set_bid.save()
                        return HttpResponse("Bid Successful")

                        
                    else:
                        return render(request, "auctions/product.html",{
                            "product": product,
                            "bidding": bidding,
                            "user_listing": user_listing,
                            "comments": comment,
                            "Max_Bid": max_bid["bid_price__max"],
                            "error":"Bid needs to be higher than the start price or previous Bid"
                        })
        if "Comment" in request.POST:
            Commenting = CommentForm(request.POST)
            if Commenting.is_valid:                
                current_comment = request.POST["comment"]
                print(comment)
                set_comment = Comment(user_listing = user_listing, comment = current_comment, user= user_comment )
                set_comment.save()
                return render(request, "auctions/product.html",{
                "product": product,
                "bidding": bidding,
                "user_listing": user_listing,
                "comments": comment,
                "Max_Bid": max_bid["bid_price__max"],
                "All_Comments": Comment.objects.all()
            })
            


    else:
        return render(request, "auctions/product.html",{
            "product": product,
            "bidding": bidding,
            "user_listing": user_listing,
            "comments": comment,
            "Max_Bid": max_bid["bid_price__max"],
            "All_Comments": Comment.objects.all()
        })


def CloseBid(request, product_id):
    return HttpResponse("The Bidding has been Closed and it is Won by")