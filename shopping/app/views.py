from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, Profile
from .forms import  CustomerProfileForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import  login , logout , authenticate
from django.contrib.auth.models import User
import uuid
from django.shortcuts import get_object_or_404

class ProductView(View):
 def get (self,request):
  topwears=Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  context={
   'topwears':topwears,
   'bottomwears':bottomwears,
   'mobiles':mobiles
  }
  return render(request,'app/home.html',context)



# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
 def get(self,request,pk):
  product= Product.objects.get(pk=pk)
  item_already_in_cart=False
  if request.user.is_authenticated:
   item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})
@login_required()
def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')
@login_required()
def show_cart(request):
 if request.user.is_authenticated:
  user=request.user
  cart = Cart.objects.filter(user=user)
  amont=0.0
  shipping_amount=70.0
  cart_product =[p for p in Cart.objects.all() if p.user==user]

  if cart_product:
   for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amont+= tempamount
    totalamont= amont+ shipping_amount

    return render(request, 'app/addtocart.html',{'cart':cart,'amont':amont,'totalamont':totalamont})
  else:
   return render(request,'app/empty.html')

def plus_cart(request):
 if request.method == 'GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amont = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amont += tempamount
  data ={
   'quantity':c.quantity,
   'amont':amont,
   'totalamont': amont + shipping_amount
  }
  return JsonResponse(data)


def minus_cart(request):
 if request.method == 'GET':
  prod_id=request.GET['prod_id']
  print(prod_id)
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amont = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amont += tempamount

  data ={
   'quantity':c.quantity,
   'amont':amont,
   'totalamont':amont+shipping_amount
  }
  return JsonResponse(data)

def remove_cart(request):
  if request.method == 'GET':
   prod_id = request.GET['prod_id']
   print(prod_id)
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.delete()
   amont = 0.0
   shipping_amount = 70.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user]
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amont += tempamount
   data = {
    'amont': amont,
    'totalamont': amont + shipping_amount
   }
   return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')
@login_required()
def address(request):
 add=Customer.objects.filter( user=request.user)
 return render(request, 'app/address.html',{'add':add ,'active':'btn-primary'})
@login_required()
def orders(request):
 op=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'op':op})


def mobile(request,data=None):
     if data==None:
       mobiles=Product.objects.filter(category='M')
     elif data == 'iphone' or data =='sumsung':
      mobiles=Product.objects.filter(category='M').filter(brand=data)
     elif data=='below':
      mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
     elif data=='above':
      mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

     return render (request, 'app/mobile.html',{'mobiles':mobiles})



# customer login system

def Login(request):
  if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            username = user.username
            return render(request, 'app/profile.html', {'fname': username})
        else:
            return redirect('home')

  return render(request, 'app/login.html')


def customerregistration(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        if User.objects.filter(username=username).first():
            messages.success(request,'username already b  exists! please try some other name  ')
            return redirect('customerregistration')
        if User.objects.filter(email=email).first():
            messages.success(request,'email already register')
            return redirect('customerregistration')
        user_obj = User.objects.create_user(username, email,password)
        user_obj.set_password(password)
        auth_token=str(uuid.uuid4())

        pro_obj = Profile.objects.create(user=user_obj,auth_token=auth_token)
        pro_obj.save()
        send_mail_registration(email,auth_token)
        return render(request, 'app/success.html')


    return render(request,'app/customerregistration.html')

def success(request):
    return render(request,'app/success.html')

def token_send(request):
    return render(request,'app/token_send.html')


# def error(request):
#     return render(request,'app/error.html')

def send_mail_registration(email,token):
    subject = "your account need to verify"
    message = f'hi click the link for verify http://127.0.0.1:8000/account-verify/{token}'
    email_from= settings.EMAIL_HOST_USER
    recipient_list =[email]
    send_mail(subject,message,email_from,recipient_list)

def verify(request,auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    profile_obj.is_verified = True
    profile_obj.save()
    messages.success(request, 'OWWO,your mail is verified')
    return redirect('login')

def signout(request):
    logout(request)
    return redirect('login')


def changepass(request):
    login_user = get_object_or_404(User, id=request.user.id)
    if "change_pass" in request.POST:
        c_password = request.POST.get('current_password')
        n_password = request.POST.get('new_pass')
        check = login_user.check_password(c_password)

        if check == True:
            login_user.set_password(n_password)
            login_user.save()
            login(request, login_user)
            return redirect('changepassworddone')
        else:
            messages.success(request,'Current Password incorrect ')
    return render(request,'app/changepassword.html')
def changepas_done(request):
    return render(request,'app/changepassworddone.html')



##########checkout

@login_required()
def checkout(request):
     user=request.user
     add=Customer.objects.filter(user=user)
     cart_item = Cart.objects.filter(user=user)
     amount=0.0
     shipping_amont=70.0
     totalamount=0.0
     cart_product = [p for p in Cart.objects.all() if p.user == request.user]
     if cart_product:
      for p in cart_product:
       tempamount = (p.quantity * p.product.discounted_price)
       amount += tempamount
      totalamount=amount+shipping_amont
     return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_item':cart_item})




###############pyment done

@login_required()
def payment_done(request):
     user=request.user
     custid = request.GET.get('custid')
     customer = Customer.objects.get(id=custid)
     cart=Cart.objects.filter(user=user)
     for c in cart:
      OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
      c.delete()
     return redirect('orders')

######Profile view

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  return  render(request,'app/profile.html',{'form':form , 'active':'btn-primary'})
 def post(self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr=request.user
   name=form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,'congratulation!! profile update successfully')
  return  render(request,'app/profile.html',{'form':form, 'active':'btn-primary'})