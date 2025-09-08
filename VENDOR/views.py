import re
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages

from management_admin.models import Category
from .models import Product, VendorRegister
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password




from django.core.paginator import Paginator, EmptyPage, InvalidPage




from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import VendorRegister


from django.db.models import Q


from USER.models import OrderItem

from USER.models import Order

from USER.models import Review
# Create your views here.

def index(request):
    vendor_email = request.session.get('vendor_email')
    vendor = None
    if vendor_email:
        try:
            vendor = VendorRegister.objects.get(email=vendor_email)
        except VendorRegister.DoesNotExist:
            vendor = None

    return render(request, "base.html", {
        "vendor": vendor,
    })

def vendor_home(request):
    return render(request,'vendor_home_page.html')

# def vendor(request):
#     return render(request,'vendor_page.html')


# def index(request):
#     return redirect('vendor_register')

def register_vendor(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        company_name = request.POST.get("company_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('vendor:vendor_register')

        
        if VendorRegister.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('vendor:vendor_register')

        
        vendor = VendorRegister(
            name=name,
            phone=phone,
            email=email,
            company_name=company_name,
            address=address,
            password=password  
        )
        vendor.save()

        # messages.success(request, "Vendor registered successfully!")
        return redirect('vendor:vendor_login')

    return render(request, "vendor_register.html")

# def index(request):
#     return render(request,'vendor_login.html')

def vendor_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            vendor = VendorRegister.objects.get(email=email)
        except VendorRegister.DoesNotExist:
            messages.error(request, "Invalid email ")
            return render(request, 'vendor_login.html')

        if check_password(password, vendor.password):
            
            request.session['vendor_id'] = vendor.id
            request.session['vendor_name'] = vendor.name
            request.session['vendor_email'] = vendor.email
            request.session['vendor_phone'] = str(vendor.phone)  
            request.session['vendor_company_name'] = vendor.company_name or ""
            request.session['vendor_address'] = vendor.address or ""
            request.session['vendor_join_date'] = vendor.join_date.strftime('%Y-%m-%d %H:%M:%S')
            # messages.success(request, "Login successful!")
            return redirect('vendor:vendor_home')  
        else:
            messages.error(request, "Invalid password.")
            return render(request, 'vendor_login.html')

    return render(request, 'vendor_login.html')

# def vendor_profile(request):
    # vendor_id = request.session.get('vendor_id')
    # if not vendor_id:
    #     # Not logged in, redirect to login page
    #     return redirect('login')

    # try:
    #     vendor = VendorRegister.objects.get(id=vendor_id)
    # except VendorRegister.DoesNotExist:
    #     # Vendor not found, clear session and redirect login
    #     request.session.flush()
    #     return redirect('login')

    # context = {
    #     'vendor': vendor,
    # }
    # return render(request, 'vendor_profile.html', context)
def vendor_profile(request):
    vendor_id = request.session.get('vendor_id')
    vendor = VendorRegister.objects.get(id=vendor_id)
    context = {'vendor': vendor}
    return render(request, 'vendor_profile.html', context)



def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(VendorRegister, id=vendor_id)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        company_name = request.POST.get("company_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        
        phone_clean = phone.replace(" ", "")  
        if not re.fullmatch(r"\+?\d{10,15}", phone_clean):
            messages.error(request, "Invalid phone number.")
            return redirect('vendor:edit_vendor', vendor_id=vendor.id)
        
        if password or confirm_password:
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('vendor:edit_vendor', vendor_id=vendor.id)
            else:
                
                vendor.password = make_password(password)

        
        vendor.name = name
        vendor.phone = phone
        vendor.email = email
        vendor.company_name = company_name
        vendor.address = address
        vendor.save()

        # messages.success(request, "Profile updated successfully!")
        return redirect('vendor:vendor_profile')

    context = {'vendor': vendor}
    return render(request, 'edit_vendor.html', context)



def vendor_logout(request):
    request.session.flush()  
    return redirect('vendor:vendor_home')


# def addproduct(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         description = request.POST.get("description")
#         price = request.POST.get("price")
#         discount = request.POST.get("discount")
#         stock = request.POST.get("stock")

#         # Get Category object
#         category_id = request.POST.get("category")
#         category = get_object_or_404(Category, id=category_id)

#         # Get uploaded files
#         image = request.FILES.get("image")
#         image2 = request.FILES.get("image2")
#         image3 = request.FILES.get("image3")

#         # Save product
#         product = Product(
#             name=name,
#             description=description,
#             price=price,
#             discount=discount,
#             stock=stock,
#             category=category,
#             image=image,
#             image2=image2,
#             image3=image3,
#         )
#         product.save()

# #        return redirect("product_list")  # redirect after saving

#     categories = Category.objects.all()
#     return render(request, "product_add.html", {"categories": categories})

    
def addproduct(request):
    vendor_id = request.session.get("vendor_id")
    if not vendor_id:
        messages.error(request, "You must be logged in as a vendor to add products.")
        return redirect("vendor:vendor_login")

    vendor = get_object_or_404(VendorRegister, id=vendor_id)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        discount = request.POST.get("discount")
        stock = request.POST.get("stock")

        
        try:
            price = float(price)
        except (TypeError, ValueError):
            price = 0

        try:
            discount = int(discount)
        except (TypeError, ValueError):
            discount = 0

        try:
            stock = int(stock)
        except (TypeError, ValueError):
            stock = 0

        # Get Category object
        # category_id = request.POST.get("category")
        # category = get_object_or_404(Category, id=category_id)

        subcategory_id = request.POST.get("subcategory")
        category = get_object_or_404(Category, id=subcategory_id)

        
        image = request.FILES.get("image")
        image2 = request.FILES.get("image2")
        image3 = request.FILES.get("image3")

        
        product = Product(
            name=name,
            description=description,
            price=price,
            discount=discount,
            stock=stock,
            category=category,
            vendor=vendor,   # 🔑 fix: assign vendor
            image=image,
            image2=image2,
            image3=image3,
        )
        product.save()

        # messages.success(request, "Product added successfully!")
        return redirect("vendor:vendor")  

    categories = Category.objects.all()
    return render(request, "product_add.html", {"categories": categories})


# def product_list(request):
#     products = Product.objects.all()
#     return render(request, "vendor_page.html", {"products": products})


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            vendor = VendorRegister.objects.get(email=email)
            token = get_random_string(30)  
            vendor.reset_token = token     
            vendor.save()

            reset_link = request.build_absolute_uri(
                f"/reset-password/{token}/"
            )

            
            send_mail(
                "Reset Your Password",
                f"Click this link to reset your password: {reset_link}",
                "prajilap01@gmail.com",
                [email],
                fail_silently=False,
            )

            messages.success(request, "Password reset link sent to your email.")
            return redirect("vendor:vendor_login")

        except VendorRegister.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect("vendor:vendor_forgot_password")

    return render(request, "forgot_password.html")

def reset_password(request, token):
    try:
        vendor = VendorRegister.objects.get(reset_token=token)
    except VendorRegister.DoesNotExist:
        messages.error(request, "Invalid or expired token.")
        return redirect("vendor:vendor_login")

    if request.method == "POST":
        password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(request.path)

        
        vendor.password = make_password(password)
        vendor.reset_token = None  
        vendor.save()

        messages.success(request, "Password reset successful. You can log in now.")
        return redirect("vendor:vendor_login")

    return render(request, "reset_password.html", {"token": token})



def vendor(request):
    vendor_email = request.session.get('vendor_email')  # Example: you saved vendor email in session
    vendor = VendorRegister.objects.get(email=vendor_email)

    
    product_list = Product.objects.filter(vendor=vendor)
    paginator = Paginator(product_list, 8)  
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request,'vendor_page.html', {'products': products,'vendor': vendor})



# def product_view(request):
#     return render(request,"product_view.html")

# def proDetail(request, c_slug, product_slug):  
#     try:
#         product = Product.objects.get(category__slug=c_slug, slug=product_slug)
#     except Exception as e:
#         raise e
#     return render(request, 'product_view.html', {'product': product})


def proDetail(request, c_slug, product_slug):
    product = get_object_or_404(Product, category__slug=c_slug, slug=product_slug)
    return render(request, 'product_view.html', {'product': product})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()  # ✅ fetch all categories

    if request.method == "POST":
        product.name = request.POST.get("name")     
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.discount = request.POST.get("discount")
        product.stock = request.POST.get("stock")
        product.category_id = request.POST["category"]  

        if "image" in request.FILES:
            product.image = request.FILES["image"]
        if "image2" in request.FILES:
            product.image2 = request.FILES["image2"]
        if "image3" in request.FILES:
            product.image3 = request.FILES["image3"]
        
        
        product.save()
        return redirect("vendor:prodCatdetail",c_slug=product.category.slug,product_slug=product.slug)

    # ✅ now categories will be available in template
    return render(request,"edit_product.html",{"product": product, "categories": categories})


# def delete_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     if request.method == "POST":  # Only delete on POST (safety)
#         product.delete()
#         return redirect("vendor:vendor_home")  # redirect after delete

#     # Optional: confirmation page
#     # return render(request, "delete_product.html", {"product": product})
#     return redirect("vendor:prodCatdetail")

def delete_product(request, product_id):
    # product = get_object_or_404(Product, id=product_id)
    # product.delete()
    # messages.success(request, "Product deleted successfully.")
    # return redirect('vendor:vendor')  # change 'vendor' to your vendor home/list view name

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.delete()
        # messages.success(request, "Product deleted successfully.")
        return redirect('vendor:vendor')  # redirect to vendor product list

    messages.error(request, "Invalid request.")
    return redirect('vendor:vendor')


# def product_search_vendor(request):
#     query = request.GET.get('q') 

#     if query:
#         products = Product.objects.filter(
#             Q(name__icontains=query) |
#             Q(description__icontains=query) |
#             Q(category__name__icontains=query)
#         )
#     else:
#         products = Product.objects.all()

#     return render(request, "vendor_page.html", {"products": products,})


def product_search_vendor(request):
    # get vendor from session
    vendor_email = request.session.get('vendor_email')
    vendor = get_object_or_404(VendorRegister, email=vendor_email)

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            vendor=vendor  # ✅ only this vendor's products
        ).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) 
            
        )
    else: 
        products = Product.objects.filter(vendor=vendor)  # ✅ only this vendor

    # Pagination (8 per page)
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, "vendor_page.html", {
        "products": products_page,
        "query": query,
        "vendor": vendor,
    })


def vendor_orders(request, vendor_id):
    vendor = get_object_or_404(VendorRegister, id=vendor_id)

    # Get only order items for this vendor's products
    order_items = OrderItem.objects.filter(product__vendor=vendor).select_related('order', 'product', 'order__user')

    # Optional: group order items by order id for display
    orders_dict = {}
    for item in order_items:
        if item.order.id not in orders_dict:
            orders_dict[item.order.id] = {
                'order': item.order,
                'items': []
            }
        orders_dict[item.order.id]['items'].append(item)

    context = {
        'vendor': vendor,
        'orders_dict': orders_dict,
    }
    return render(request, 'vendor_orders.html', context)


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        if order.status != "Cancelled" and order.status != "Delivered":
            order.status = "Cancelled"
            order.save()
            messages.success(request, f"Order #{order.id} has been cancelled.")
        else:
            messages.info(request, "This order cannot be cancelled.")

    # Get vendor from first item in order
    first_item = order.items.first()  # adjust 'items' if your related_name is different
    vendor_id = first_item.product.vendor.id

    return redirect('vendor:vendor_orders', vendor_id)



def vendor_reviews(request):
    vendor_email = request.session.get('vendor_email')  # Example: you saved vendor email in session
    vendor = VendorRegister.objects.get(email=vendor_email)

    # fetch only products of this vendor
    product_list = Product.objects.filter(vendor=vendor)
    paginator = Paginator(product_list, 12)  
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request,'vendor_reviews.html', {'products': products,'vendor': vendor})

def vendor_review_detail(request, product_id):
    vendor_email = request.session.get('vendor_email')
    vendor = VendorRegister.objects.get(email=vendor_email)

    # fetch product (only if it belongs to this vendor)
    product = get_object_or_404(Product, id=product_id, vendor=vendor)

    # fetch product reviews
    reviews = Review.objects.filter(product=product)

    return render(request, 'vendor_review_detail.html', {
        'product': product,
        'reviews': reviews,
        'vendor': vendor
    })