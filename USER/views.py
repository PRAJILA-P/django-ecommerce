from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from . models import Register
from VENDOR.models import Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from management_admin.models import Category

from django.db.models import Q

from . models import Cart


from .models import Order, OrderItem
from .forms import CheckoutForm

from django.contrib.auth.decorators import login_required


from .forms import ReviewForm

from .models import Review
# Create your views here.

# def index(request):
#     return render(request,'index.html')


def user_register(request):
    if request.method=='POST':
        name=request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        gender=request.POST.get("gender")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request,"password does'nt match")
            return redirect('user:user_register.html')
        Register.objects.create(name=name,phone=phone,email=email,gender=gender,password=password )
        # messages.success(request, "Account created successfully!")
        return redirect('user:user_login') 
    return render(request,'user_register.html')


        
def user_login(request):
    if request.method=='POST':
        email=request.POST.get("email")
        password=request.POST.get("password")

        try:
            user=Register.objects.get(email=email)
        except Register.DoesNotExist:
            messages.error(request,'invalid email')
            return redirect('user:user_login')    
        if user.password==password:
            request.session['user_id']=user.id
            request.session['user_name']=user.name
            request.session['user_email'] = user.email
            request.session['user_phone'] = str(user.phone) 
            request.session['user_gender'] = user.get_gender_display()

            return redirect('user:index')
        else:
            messages.error(request,'password incorrect')
            return redirect('user:user_login')
        
    return render(request,'user_login.html')    


def user_profile(request):
    user_id = request.session.get('user_id')
    user = Register.objects.get(id=user_id)
    context = {'user': user}
    return render(request, 'user_profile.html', context)

def user_logout(request):
    request.session.flush()
    return redirect('user:index')

def user_edit_profile(request,user_id):
    user=get_object_or_404(Register,id=user_id)

    if request.method=="POST":
        name=request.POST.get('name')
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        gender=request.POST.get("gender")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        try:
            phone=int(phone)
        except ValueError:
            messages.error(request,"Invalid phone number")
            return redirect('user:user_edit_profile',user_id=user.id)
    
        if password != confirm_password:
            messages.error(request,"Passwords do not match.")
            return redirect('user:user_edit_profile',user_id=user.id)
    
        user.name = name
        user.phone = phone
        user.email = email
        user.gender = gender
        user.password = password
        user.save()

        return redirect('user:user_profile')
    
    context={'user':user}
    return render(request,'user_edit_profile.html',context)
        

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, "index.html", {"products": products})


def index(request):
    categories = Category.objects.all()
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 8)  
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, "home.html", {"categories": categories,"products": products})

# def products_by_category(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     products = Product.objects.filter(category=category)
#     return render(request, "products_by_category.html", {
#         "category": category,
#         "products": products
#     })

# def products_by_category(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)

#     # Include products from this category + its direct subcategories
#     subcategories = Category.objects.filter(parent=category)
#     products = Product.objects.filter(category__in=[category] | list(subcategories))

#     return render(request, "products_by_category.html", {
#         "category": category,
        
#         "products": products
#     })


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    # Category + its subcategories
    categories = Category.objects.filter(Q(id=category.id) | Q(parent=category))
    product_list = Product.objects.filter(category__in=categories)
    
    paginator = Paginator(product_list, 8)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    return render(request, "category.html", {
        "category": category,
        "products": products
    })


# def prodCatdetail(request, category_slug, product_slug):
#     product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
#     return render(request, "product.html", {"product": product})


def prodCatdetail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    reviews = Review.objects.filter(product=product).order_by("-created_at")
    return render(request, "product.html", {
        "product": product,
        "reviews": reviews,
    })


# def prodCatdetail(request, category_slug, product_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     product = get_object_or_404(Product, category=category, slug=product_slug)

#     return render(request, "product_detail.html", {
#         "category": category,
#         "product": product,
#     })


# def category_view(request, category_slug):
#     # Get the main category (like jewellery)
#     category = get_object_or_404(Category, slug=category_slug, parent=None)

#     # Get all subcategories of this main category
#     subcategories = category.subcategories.all()

#     # Get all products that belong either to the main category or its subcategories
#     products = Product.objects.filter(category__in=[category] + list(subcategories))

#     context = {
#         "category": category,
#         "subcategories": subcategories,
#         "products": products,
#     }
#     return render(request, "category.html", context)


def add_to_cart(request, product_id):
    register_id = request.session.get("user_id")
    if not register_id:
        messages.error(request, "You must be logged in to add items to cart.")
        return redirect("user:user_login")  # change to your login url name

    user = get_object_or_404(Register, id=register_id)
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("user:view_cart")


def view_cart(request):
    register_id = request.session.get("user_id")
    if not register_id:
        messages.error(request, "You must be logged in to view cart.")
        return redirect("user:user_login")

    user = get_object_or_404(Register, id=register_id)
    cart_items = Cart.objects.filter(user=user)
    total = sum(item.total_price() for item in cart_items)

    return render(request, "cart.html", {"cart_items": cart_items, "total": total})


def remove_from_cart(request, cart_id):
    user_id = request.session.get("user_id")
    cart_item = get_object_or_404(Cart, id=cart_id, user_id=user_id)
    cart_item.delete()
    return redirect("user:view_cart")



def update_quantity(request, cart_id, action):
    user_id = request.session.get("user_id")   # adjust key as per your login system
    cart_item = get_object_or_404(Cart, id=cart_id, user_id=user_id)

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1

    cart_item.save()
    return redirect("user:view_cart")


# def checkout(request):
#     """Convert cart items into an order"""
#     user_id = request.session.get("user_id")   # assuming you store user in session
#     if not user_id:
#         messages.error(request, "Please login first")
#         return redirect("user:user_login")

#     user = get_object_or_404(Register, id=user_id)
#     cart_items = Cart.objects.filter(user=user)

#     if not cart_items:
#         messages.error(request, "Your cart is empty")
#         return redirect("user:view_cart")

#     if request.method == "POST":
#         address = request.POST.get("address")
#         city = request.POST.get("city")
#         state = request.POST.get("state")
#         postal_code = request.POST.get("postal_code")

#         # 1. Create the Order
#         order = Order.objects.create(
#             user=user,
#             address=address,
#             city=city,
#             state=state,
#             postal_code=postal_code,
#         )

#         # 2. Move Cart items → OrderItem
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 price=item.product.price
#             )

#         # 3. Clear the cart
#         cart_items.delete()

#         messages.success(request, f"Order {order.id} placed successfully!")
#         return redirect("user:order_detail", order_id=order.id)

#     return render(request, "checkout.html", {"cart_items": cart_items})

def checkout(request):
    # ✅ Fetch logged-in custom user from session
    user_id = request.session.get("user_id")  # or "user_email" if you stored email
    if not user_id:
        return redirect("user:user_login")  # not logged in

    user = get_object_or_404(Register, id=user_id)

    cart_items = Cart.objects.filter(user=user)


    if not cart_items.exists():
        # messages.error(request,"your cart is empty")
        return redirect("user:view_cart")  # or show a message



    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # ✅ Create order for this Register user
            order = Order.objects.create(
                user=user,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data['country'],
            )

            # ✅ Move cart items into order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,  # keep purchase price
                )

            # ✅ Clear cart
            cart_items.delete()

            return redirect("user:order_detail", order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {"form": form, "cart_items": cart_items})
# def order_list(request):
#     """Show all orders of logged-in user"""
#     user_id = request.session.get("user_id")
#     user = get_object_or_404(Register, id=user_id)
#     orders = Order.objects.filter(user=user).order_by("-created_at")
#     return render(request, "orders.html", {"orders": orders})

# def order_list(request,order_id):
#     user_id = request.session.get("user_id")
#     if not user_id:
#         return redirect("user:user_login")

#     order = get_object_or_404(Order, id=order_id, user_id=user_id)
#     return render(request, "user_order.html", {"order": order})


# @login_required
def order_list(request):
    # 1️⃣ Get user id from session
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("user:user_login")

    # 2️⃣ Fetch Register instance
    user = get_object_or_404(Register, id=user_id)

    # 3️⃣ Filter orders
    orders = Order.objects.filter(user=user).order_by("-created_at")

    # 4️⃣ Calculate subtotal for items
    # for order in orders:
    #     for item in order.items.all():
    #         item.subtotal = item.price * item.quantity

    return render(request, "user_order.html", {"orders": orders})

def order_detail(request, order_id):
    """Show single order details"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order.html", {"order": order})

# def add_review(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     # ✅ get logged-in Register user from session
#     register_id = request.session.get("user_id")
#     if not register_id:
#         messages.error(request, "You must be logged in to submit a review.")
#         return redirect("user:user_login")

#     register_user = get_object_or_404(Register, id=register_id)

#     if request.method == "POST":
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.product = product
#             review.user = register_user   # ✅ assign Register instance
#             review.save()
#             messages.success(request, "Review submitted successfully!")
#             return redirect("user:prodCatdetail", category_slug=product.category.slug, product_slug=product.slug)
#     else:
#         form = ReviewForm()

#     return render(request, "add_review.html", {"form": form, "product": product})


def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # ✅ get logged-in Register user from session
    register_id = request.session.get("user_id")
    if not register_id:
        messages.error(request, "You must be logged in to submit a review.")
        return redirect("user:user_login")

    register_user = get_object_or_404(Register, id=register_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            comment = form.cleaned_data["comment"]

            # ✅ Check if user already reviewed this product
            existing_review = Review.objects.filter(user=register_user, product=product).first()

            if existing_review:
                # update instead of creating duplicate
                existing_review.rating = rating
                existing_review.comment = comment
                existing_review.save()
                messages.success(request, "Your review has been updated.")
            else:
                # create new review
                Review.objects.create(
                    user=register_user,
                    product=product,
                    rating=rating,
                    comment=comment,
                )
                messages.success(request, "Your review has been submitted.")

            return redirect("user:prodCatdetail", category_slug=product.category.slug, product_slug=product.slug)

    else:
        form = ReviewForm()

    return render(request, "add_review.html", {"form": form, "product": product})




def cancel_order(request, order_id):
    # Ensure user is logged in (using your session key 'user_id')
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "Please login first to cancel an order.")
        return redirect("user:user_login")

    # Verify the logged-in user exists
    try:
        user = Register.objects.get(id=user_id)
    except Register.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("user:user_login")

    # Fetch the order only if it belongs to this user
    order = get_object_or_404(Order, id=order_id, user=user)

    if order.status not in ["Cancelled", "Delivered"]:
        order.status = "Cancelled"
        order.save()
        messages.success(request, f"Order #{order.id} has been cancelled successfully.")
    else:
        messages.warning(request, "This order cannot be cancelled.")

    return redirect("user:order_list")

def product_search(request):
    query = request.GET.get("q")
    categories = Category.objects.all()

    if query:
        # get categories matching the query (both main & sub)
        matching_categories = Category.objects.filter(
            Q(name__icontains=query) | Q(slug__icontains=query)
        )

        # include products in those categories + their subcategories
        product_list = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__in=matching_categories) |
            Q(category__parent__in=matching_categories)  # ✅ include parent match
        ).distinct()
    else:
        product_list = Product.objects.all()

    # Pagination
    paginator = Paginator(product_list, 8)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "query": query,
    })


