from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from . models import Register
from VENDOR.models import Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from management_admin.models import Category

from django.db.models import Q
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
    products = Product.objects.filter(category__in=categories)

    return render(request, "category.html", {
        "category": category,
        "products": products
    })

def prodCatdetail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)

    return render(request, "product_detail.html", {
        "category": category,
        "product": product,
    })


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