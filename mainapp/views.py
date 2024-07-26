from django.shortcuts import render
from .models import * 
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.messages import error,success
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from random import randint

from django.conf import settings
from django.core.mail import send_mail

from supershop.settings import RAZORPAY_API_KEY ,RAZORPAY_API_SECRET_KEY
import razorpay
# from .client import Client

# Create your views here.
def homepage(Request):
    products= Product.objects.all().order_by('-id')[0:12]
    testimonial = Testimonial.objects.all().order_by("-id")

    return render(Request,'index.html',{"products":products,"testimonial":testimonial })

def aboutpage(Request):
    return render(Request,'about.html')

# @login_required(login_url="/login/")

#       =====>  using session <=====
def addToCartPage(Request):
    if(Request.method=='POST'):
        # del Request.session['cart']
        cart=Request.session.get('cart',None)
        qty= int(Request.POST.get('qty'))
        id=Request.POST.get('id')
        try:
            p=Product.objects.get(id=id)
            if(cart):
                if (str(id) in cart.keys()):
                    item= cart[str(id)]
                    item['qty'] = item['qty']+qty
                    item['total'] = item['total']+qty*item['price']
                    cart[str(id)] = item
                else:
                    cart.setdefault(str(id),{'productid':id,'name':p.name,'brand':p.brand.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':qty,'total':qty*p.finalprice,'pic':p.pic1.url} )
            else:
                
                    p=Product.objects.get(id=id)
                
                    cart={str(id):{'productid':id,'name':p.name,'brand':p.brand.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':qty,'total':qty*p.finalprice,'pic':p.pic1.url}  }
        
        
            Request.session['cart']=cart
            Request.session.set_expiry(60*60*24*30)
        except:
            pass
    return HttpResponseRedirect("/cart/")

# @login_required(login_url="/login/")
def cartpage(Request):
    cart=Request.session.get('cart',None)
    subtotal=0
    shipping=0
    total=0
    if (cart):
        for value in cart.values():
            subtotal = subtotal + value['total']
        if(subtotal > 0 and subtotal<1000):
            shipping=150
        total = subtotal+ shipping
    return render(Request,'cart.html',{'cart':cart,'subtotal':subtotal,"shipping":shipping,'total':total})

def deleteCart(Request,id):
    cart= Request.session.get("cart",None)
    if(cart):
     del cart[id]   
     Request.session['cart']=cart

    else:
        pass
    
    return HttpResponseRedirect("/cart/")


def updateCartpage(Request,id,op):
    cart= Request.session.get("cart",None)
    if(cart):
        item= cart[id]
        if(op=="dec" and item['qty']==1):
            return HttpResponseRedirect("/cart/")
        else:
            if(op=='dec'):
                item['qty']=item['qty']-1
                item['total']=item['total']-item['price']
            else:
                item['qty']=item['qty']+1
                item['total']=item['total']+item['price']
        cart[id]=item
        Request.session['cart']=cart
    else:
        pass
    
    
    return HttpResponseRedirect("/cart/")





def contactpage(Request):
    if (Request.method=='POST'):
        c = Contact()
        c.name=Request.POST.get("name")
        c.email=Request.POST.get("email")
        c.phone=Request.POST.get("phone")
        c.subject=Request.POST.get("subject")
        c.message=Request.POST.get("message")
        c.save()
        success(Request,"Thanks to Share Your Query With Us!! Our Team Will Contact You Soon ")
    return render(Request,'contact.html')


# def loginpage(Request):

#     return render(Request,'login.html')


def signuppage(Request):
    return render(Request,'signup.html')


def shoppage(Request ,mc,sc,br):
    if(mc=="All" and sc=="All" and br=="All"):
        products= Product.objects.all().order_by('-id')
    
    # for filter all routs 

    elif(mc!="All" and sc=="All" and br=="All"):
        products= Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by('-id')

    elif(mc=="All" and sc!="All" and br=="All"):
        products= Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by('-id')
    
    elif(mc=="All" and sc=="All" and br!="All"):
        products= Product.objects.filter(brand=Brand.objects.get(name=br)).order_by('-id')

    
    # (mc!="All" and sc!="All" and br!="All"):
    
    elif(mc!="All" and sc!="All" and br=="All"):
        products= Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by('-id').order_by('-id')

    
    elif(mc!="All" and sc=="All" and br!="All"):
        products= Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br)).order_by('-id').order_by('-id') 
    
    elif(mc=="All" and sc!="All" and br!="All"):
        products= Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br)).order_by('-id').order_by('-id') 
    

    # (mc!="All" and sc!="All" and br!="All"):
    else:
        products= Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br)).order_by('-id').order_by('-id') 
    
    

    maincategory = Maincategory.objects.all().order_by("-id")
    subcategory = Subcategory.objects.all().order_by("-id")
    brand = Brand.objects.all().order_by("-id")

    return render(Request,'shop.html',{'products':products , "maincategory":maincategory , "subcategory":subcategory, "brand":brand,'mc':mc, 'sc':sc, "br":br})


def searchPage(Request):
    if Request.method == "POST":
        search =  Request.POST.get("search")
        try:
            maincategory= Maincategory.objects.get(name=search)
        except:
            maincategory = None

        try:
            subcategory= Subcategory.objects.get(name=search)
        except:
            subcategory = None

        try:
            brand= Brand.objects.get(name=search)
        except:
            brand = None


        products = Product.objects.filter(Q(name__icontains = search)|Q(maincategory = maincategory)|Q(subcategory =subcategory)|Q(brand = brand)|Q(color= search))
        maincategory = Maincategory.objects.all().order_by("-id")
        subcategory = Subcategory.objects.all().order_by("-id")
        brand = Brand.objects.all().order_by("-id")

        return render(Request,'shop.html',{'products':products , "maincategory":maincategory , "subcategory":subcategory, "brand":brand,'mc':"All", 'sc':"All", "br":"All"})
    else : return  HttpResponseRedirect("/")



def singleproductpage(Request,id):
    product=Product.objects.get(id=id)
    return render(Request,'single-product.html',{"product":product})



def loginpage(Request):
    if(Request.method=="POST"):
        username= Request.POST.get("username")
        password= Request.POST.get("password")
        user = authenticate(username=username,password=password)
        if (user is not None):
            login(Request,user)

            if(user.is_superuser):
            
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        
        else:
            error(Request,"Invalid Username or password ")
    return render(Request,'login.html')


def signuppage(Request):

    if (Request.method == 'POST'):
        # b= Buyer
        # b.name = Request.POST.get("name")
        
        password = Request.POST.get("password")
        cpassword = Request.POST.get("cpassword")
        if(password == cpassword):
            username = Request.POST.get("username")
            email = Request.POST.get("email")
            name = Request.POST.get("name")
            try:
                User.objects.create_user(username=username,email=email,password=password,first_name=name)

                phone = Request.POST.get("phone")

                b= Buyer()
                b.name=name
                b.email=email
                b.username = username
                b.phone = phone
                b.save()
                return HttpResponseRedirect('/login/')
            except:
                error(Request,"UserName Already Taken !!!")
        else:
            error(Request, "Password and confirm password DoesN't Match ")

    return render(Request,'signup.html')

@login_required(login_url="/login/")
def logoutpage(Request):
    logout(Request)
    return HttpResponseRedirect("/login/")

# @login_required(login_url="/login/")
def profilepage(Request):
    if(Request.user.is_superuser):
        return HttpResponseRedirect("/admin/")
    
    # username=Request.user.username
    try:
        buyer = Buyer.objects.get(username=Request.user.username)
        wishlist = Wishlist.objects.filter(buyer=buyer)
        checkout = Checkout.objects.filter(buyer=buyer)
        orders = [] 
        for item in checkout:
            cp = CheckoutProduct.objects.filter(checkout=item)
            orders.append({'checkout':item,'cp':cp})



        return render(Request,"profile.html",{'buyer':buyer , "wishlist":wishlist,'orders':orders})
    
    except:
        
        return HttpResponseRedirect("/login/")


def updateprofilepage(Request):
    if(Request.user.is_superuser):
        return HttpResponseRedirect("/admin/")
    username=Request.user.username
    try:
        buyer = Buyer.objects.get(username=username)
        if(Request.method == "POST"):
            buyer.name=Request.POST.get("name")
            buyer.email=Request.POST.get("email")
            buyer.phone=Request.POST.get("phone")
            buyer.address=Request.POST.get("address")
            buyer.pin=Request.POST.get("pin")
            buyer.city=Request.POST.get("city")
            buyer.state=Request.POST.get("state")
            if(Request.FILES.get("pic")):
                buyer.pic=Request.FILES.get("pic")
            buyer.save()
            return HttpResponseRedirect("/profile")
        return render(Request,"updateprofile.html",{'buyer':buyer})
    
    except:
        
        return HttpResponseRedirect("/login/")
   
@login_required(login_url="/login/")
def addToWishlistpage(Request,id):
  
    buyer=Buyer.objects.get(username=Request.user.username)
    product=Product.objects.get(id=id)

    try:
        w=Wishlist.objects.get(product=product,buyer=buyer)
    except:
        w=Wishlist()
        w.product=product
        w.buyer=buyer
        w.save()
   
    return HttpResponseRedirect("/profile")
    

@login_required(login_url="/login/")
def deletewishlistpage(Request,id):
    try:
        w = Wishlist.objects.get(id=id)
        w.delete()
    except:
        pass
    return HttpResponseRedirect("/profile/")


client= razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url="/login/")
def checkoutpage(Request):

    try:
        buyer = Buyer.objects.get(username=Request.user.username)
        cart=Request.session.get('cart',None)
        subtotal=0
        shipping=0
        total=0
        if (cart):
            for value in cart.values():
                subtotal = subtotal + value['total']
            if(subtotal > 0 and subtotal<1000):
                shipping=150
            total = subtotal+ shipping

            # placed order or payment
            if(Request.method == 'POST'):
                mode = Request.POST.get("mode")
                checkout = Checkout()
                checkout.buyer=buyer
                checkout.subtotal=subtotal
                checkout.total=total
                checkout.shipping=shipping
                checkout.paymantmode=mode
                checkout.save()

                for key,value in cart.items():
                    p=Product.objects.get(id=int(key))
                    cp = CheckoutProduct()
                    cp.checkout= checkout
                    cp.product= p
                    cp.qty = value['qty']
                    cp.total = value['total']
                    cp.save()
                    # Request.session['cart']={}

                if(mode == "COD"):
                    return HttpResponseRedirect("/confirmation")
                else:
                    orderAmount=checkout.total*100
                    orderCurrency="INR"
                    paymantOrder=client.order.create(dict(amount=orderAmount,currency=orderCurrency, payment_capture='0'))
                    paymantId = paymantOrder["id"]
                    checkout.paymantmode=1
                    checkout.save()
                    return render(Request,"pay.html",{
                        "amount":orderAmount,
                        "api_key":RAZORPAY_API_KEY,
                        "order_id":paymantId,
                        "user":buyer,
                        "id":checkout.id})
                # return HttpResponseRedirect("/confirmation")
        return render(Request,"checkout.html",{'buyer':buyer,'subtotal':subtotal,"shipping":shipping,'total':total,'cart':cart})
    except:
        return HttpResponseRedirect("/admin/")


@login_required(login_url='/login/')
def rePaymentpage(Request,id):
    try:
        checkout=Checkout.objects.get(id=id)
        buyer = Buyer.objects.get(username=Request.user.username)
        orderAmount=checkout.total*100
        orderCurrency="INR"
        paymantOrder=client.order.create(dict(amount=orderAmount,currency=orderCurrency, payment_capture='0'))
        paymantId = paymantOrder["id"]
        checkout.paymantmode=1
        checkout.save()
        return render(Request,"pay.html",{
            "amount":orderAmount,
            "api_key":RAZORPAY_API_KEY,
            "order_id":paymantId,
            "user":buyer,
            "id":id})
        
    
    except:
        return HttpResponseRedirect("/profile/")
    
@login_required(login_url='/login/')
def paymentSuccesspage(Request,id,rppid,rpoid,rpsid):
    
    check = Checkout.objects.get(id=id)

    check.rppid=rppid
    check.paymantstatus=1
    check.save()
    return HttpResponseRedirect("/confirmation/")


  



# ====> error in my code <=====
# @login_required(login_url="/login/")
# def confirmationpage(Request):
#     # try:
#         buyer = Buyer.objects.get(username=Request.user.username)
#         checkout = Checkout.objects.filter(buyer=buyer).order_by("-id").first()
        
#         cart=CheckoutProduct.objects.filter(checkout = Checkout.objects.get(id = checkout.id))
        
#         subtotal=0
#         shipping=0
#         total=0
#         print(cart,"/n/n/n/n")
#         for item in cart:
#             subtotal = subtotal + item.total
#         if(subtotal > 0 and subtotal<1000):
#                 shipping=150
#         total = subtotal+ shipping
        
#         return render(Request,'confirmation.html',{'cart':cart,'subtotal':subtotal,'shipping':shipping,'total':total,'buyer':buyer,'checkout':checkout})

    
#     # except:
#     #     return HttpResponseRedirect("/admin/")




@login_required(login_url="/login/")
def confirmationpage(Request):
    try:
        buyer = Buyer.objects.get(username=Request.user.username)
        checkout = Checkout.objects.filter(buyer=buyer).order_by("-id").first()
        
        # cart=Request.session.get("cart",None)
        cart=Request.session.get('cart',None)
        subtotal=0
        shipping=0
        total=0
        if(cart):
            for value in cart.values():
                subtotal = subtotal + value['total']
            if(subtotal > 0 and subtotal<1000):
                shipping=150
            total = subtotal+ shipping

       



        # print(checkout,"\n\n\n\n\n\n\n")
        # print(checkout.paymantmode,"\n\n\n\n\n\n\n")
        Request.session['cart']={}
        return render(Request,'confirmation.html',{'cart':cart,'subtotal':subtotal,'shipping':shipping,'total':total,'buyer':buyer,'checkout':checkout})

    
    except:
        return HttpResponseRedirect("/admin/")


def newslatteSubscribePage(Request):
    if (Request.method=='POST'):
        email=Request.POST.get("email")
        n= Newslatter()
        n.email=email
        try:
            n.save()
            success(Request,"Thanks, your Are Successfull Subscribed!!! ")
        except:
            error(Request,"your email id is Already Subscribed!!! ")
        return HttpResponseRedirect("/")   
    else:
        return HttpResponseRedirect("/")
    
def forgetPassword1Page(Request):
    if Request.method == "POST":
        username = Request.POST.get("username")
        try:
            buyer = Buyer.objects.get(username=username)
            otp = randint(100000,999999)
            buyer.otp = otp 
            buyer.save()
            subject="otp for password reset "
            message=""" Hello """+buyer.name+"""
                    OTP for Password Reset is """+str(otp)+"""
                    Please Never Share Your OTP With AnyOne  
                    """
            email_from=settings.EMAIL_HOST_USER
            recipient_list = [buyer.email,]
            send_mail(subject,message,email_from,recipient_list)
            Request.session['reset-password-user'] = buyer.username
            return HttpResponseRedirect("/forget_password_2/")
        except:
            error(Request,"User Name Not Found ")
    return render(Request,"forget_password_1.html")

def forgetPassword2Page(Request):

    username= Request.session.get("reset-password-user")
    if Request.method =="POST":
      
        otp= int(Request.POST.get("otp"))
        buyer=Buyer.objects.get(username=username)
        if(otp == buyer.otp):
            return HttpResponseRedirect("/forget_password_3/")
        else:
            error(Request,"Invalid OTP")
    if username:
        return render(Request,"forget_password_2.html")
    else:
        return HttpResponseRedirect("/forget_password_1/")
    
def forgetPassword3Page(Request):
    username= Request.session.get("reset-password-user")
    if Request.method =="POST":
        
        password=Request.POST.get("password")
        cpassword=Request.POST.get("cpassword")
        if (password==cpassword):
            user=User.objects.get(username=username)
            user.set_password(password)
            user.save()
            del Request.session["reset-password-user"]
            return HttpResponseRedirect("/login/")
        else:
            error(Request,"Password and Confirm Password are not match ")
        
    if username:
        return render(Request,"forget_password_3.html")
    else:
        return HttpResponseRedirect("/forget_password_1/")


