from django.contrib import messages 
from django.shortcuts import get_object_or_404, render,redirect

from VENDOR.models import Product, VendorRegister
from USER.models import Order, OrderItem, Register, Review

from .models import Category

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .forms import ProductForm


from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

from .forms import CategoryForm  

from decimal import Decimal
# Create your views here.

# def add_category(request):
    # categories = Category.objects.all()
    # return render(request, 'product_add.html', {'categories': categories}) 



# custom_admin/views.py
# Only allow staff/admins



def custom_admin_home(request):
    return render(request,'custom_admin_home.html')



def is_admin_user(user):
    return user.is_authenticated and user.is_staff

def custom_admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect("ad_min:custom_admin_home")
    return render(request, "custom_admin_login.html")

def custom_admin_logout(request):
    logout(request)
    return redirect("ad_min:custom_admin_home")


    

    
    
def custom_admin_user(request):
    user = Register.objects.all()
    context = {'user': user}
    return render(request, 'custom_admin_user.html', context)

def custom_admin_user_edit(request, user_id):
    user = get_object_or_404(Register, id=user_id)

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.phone = request.POST.get("phone")
        user.email = request.POST.get("email")
        user.gender = request.POST.get("gender")
        user.password = request.POST.get("password")  # plain password

        user.save()
        messages.success(request, "User updated successfully!")
        return redirect("ad_min:custom_admin_user")

    context = {"user": user}
    return render(request, "custom_admin_user_edit.html", context)


def custom_admin_user_delete(request, user_id):
    user = get_object_or_404(Register, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect("ad_min:custom_admin_user")


@login_required(login_url="ad_min:custom_admin_login")
@user_passes_test(is_admin_user)
def custom_admin_dashboard(request):
    
    categories = Category.objects.all()
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 21)  
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, "custom_adimn_dashboard.html",{"categories": categories,"products": products})




def custom_admin_product(request,pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' was changed successfully.")
            return redirect('ad_min:custom_admin_dashboard')  
    else:
        form = ProductForm(instance=product)

    return render(request, 'custom_admin_product.html', {'form': form, 'product': product})

def custom_admin_product_delete(request,pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request,"deleted product successfully")
    return redirect('ad_min:custom_admin_dashboard')
    


def custom_admin_vendor(request):
    vendor = VendorRegister.objects.all()
    context = {'vendor': vendor}
    return render(request, 'custom_admin_vendor.html', context)

def custom_admin_vendor_edit(request, vendor_id):
    vendor = get_object_or_404(VendorRegister, id=vendor_id)

    if request.method == "POST":
        vendor.name = request.POST.get("name")
        vendor.phone = request.POST.get("phone")
        vendor.email = request.POST.get("email")
        vendor.company_name = request.POST.get("company_name")
        vendor.address = request.POST.get("address")

        password = request.POST.get("password")
        if password:  
            vendor.password = make_password(password)

        vendor.save()
        messages.success(request, f"Vendor {vendor.name} updated successfully!")
        return redirect('ad_min:custom_admin_vendor')  

    context = {'vendor': vendor}
    return render(request, 'custom_admin_vendor_edit.html', context)

def custom_admin_vendor_delete(request, vendor_id):
    vendor = get_object_or_404(VendorRegister, id=vendor_id)
    vendor.delete()
    messages.success(request, f"Vendor {vendor.name} deleted successfully!")
    return redirect('ad_min:custom_admin_vendor')


        
# List all categories
def custom_admin_category_list(request):
    categories = Category.objects.all()
    return render(request, "custom_admin_category_list.html", {"categories": categories})


# Add new category
def custom_admin_category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect("ad_min:category_list")
    else:
        form = CategoryForm()
    return render(request, "custom_admin_category_form.html", {"form": form, "title": "Add Category"})


# Edit category
def custom_admin_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("ad_min:category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "custom_admin_category_form.html", {"form": form, "title": "Edit Category"})


def custom_admin_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, f"Category '{category.name}' deleted successfully!")
    return redirect("ad_min:category_list")

def custom_admin_order_list(request):
    orders = Order.objects.all()
    return render(request, "custom_admin_order.html", {"orders": orders})

def custom_admin_order_detail(request,order_id):
    order=get_object_or_404(Order,id=order_id)

    if request.method=="POST":
        order.address = request.POST.get("address")
        order.city = request.POST.get("city")
        order.state = request.POST.get("state")
        order.postal_code = request.POST.get("postal_code")
        order.country = request.POST.get("country")
        order.status = request.POST.get("status")
        order.save()
        messages.success(request, f"Order #{order.id} updated successfully!")
        return redirect("ad_min:custom_admin_order_list")
    return render(request,"custom_admin_order_detail.html",{"order":order})


def custom_admin_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, f"Order  deleted successfully!")
    return redirect("ad_min:custom_admin_order_list")


def custom_admin_order_item_list(request):
    orderitems=OrderItem.objects.all()
    return render(request,"custom_admin_order_item_list.html",{"orderitems": orderitems})


# def custom_admin_order_item_detail(request, pk):
#     item = get_object_or_404(OrderItem, pk=pk)

#     if request.method == "POST":
#         item.quantity = request.POST.get("quantity")
#         item.price = request.POST.get("price")
#         item.save()
#         messages.success(request, "Order Item updated successfully.")
#         return redirect("ad_min:custom_admin_order_item_list")

#     return render(request, "custom_admin_order_item_detail.html", {"item": item})


def custom_admin_order_item_detail(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)

    if request.method == "POST":
        # Get and convert values safely, fall back to current values if invalid
        try:
            quantity = int(request.POST.get("quantity", item.quantity))
            price = Decimal(request.POST.get("price", item.price))
        except (ValueError, TypeError):
            messages.error(request, "Invalid input for quantity or price.")
            return redirect(request.path)

        status = request.POST.get("status")
        if status not in dict(OrderItem.STATUS_CHOICES):
            messages.error(request, "Invalid status selected.")
            return redirect(request.path)

        # Update fields
        item.quantity = quantity
        item.price = price
        item.status = status
        # item.subtotal = price * quantity
        item.save()

        messages.success(request, "Order Item updated successfully.")
        return redirect("ad_min:custom_admin_order_item_list")

    return render(request, "custom_admin_order_item_detail.html", {"item": item})

def custom_admin_order_item_delete(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)
    item.delete()
    messages.success(request, "Order Item deleted successfully.")
    return redirect("ad_min:custom_admin_order_item_list")

def custom_admin_review_list(request):
    reviews=Review.objects.all()
    return render(request,'custom_admin_review_list.html',{'reviews':reviews})

def custom_admin_review_detail(request, review_id):
    review=get_object_or_404(Review,id=review_id)

    if request.method=="POST":
        review.rating = request.POST.get("rating", review.rating)
        review.comment = request.POST.get("comment", review.comment)
        review.save()
        messages.success(request, "Review updated successfully!")
        return redirect("ad_min:custom_admin_review_list")

    return render(request, "custom_admin_review_detail.html", {"review": review})


def custom_admin_review_delete(request, review_id):
    review=get_object_or_404(Review,id=review_id)
    review.delete()
    messages.success(request, "Review deleted successfully!")
    return redirect("ad_min:custom_admin_review_list")


def orderitem_to_order(request, orderitem_id):
    orderitem = get_object_or_404(OrderItem, id=orderitem_id)
    order = orderitem.order  # get the related order
    return redirect('ad_min:custom_admin_order_detail', order_id=order.id)




