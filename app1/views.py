from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from . models import Registration
from . models import Contact
from . models import Cart
from . models import Addtoproduct,Order,Booktable


# Create your views here.

def index(request):
    prods = Addtoproduct.objects.all().values()
    context = {
        'products': prods,
    }
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def booktable(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    if request.method == "POST":
        date = request.POST["date"]
        time =  request.POST["time"]
        seats =  request.POST["seats"]
        place =  request.POST["place"]
        food =  request.POST["food"]

        book = Booktable(
            date = date,
            time = time,
            seats = seats,
            place = place,
            food = food,
            user = request.session['usersession']
        )
        
        book.save()





    template = loader.get_template("booktable.html")
    return HttpResponse(template.render({},request))


def index(request):
    if request.method == "POST":
        cname = request.POST["con_name"]
        cemail = request.POST["con_email"]
        cnum = request.POST["con_num"]
        carea = request.POST["con_area"]

        con = Contact(
            con_name = cname,
            con_email = cemail,
            con_num = cnum,
            con_area = carea
        )
        con.save()
    prods = Addtoproduct.objects.all().values()
    context = {
        'products': prods,
    }
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def registration(request):
    if request.method == "POST":
        rname = request.POST["regi_name"]
        remail = request.POST["regi_email"]
        rpsw = request.POST["regi_psw"]

        exist = Registration.objects.filter(regi_email = remail)
        if exist:
            request.session['errormsg'] ='errormsg'
        else:
            if 'errormsg' in request.session:
                del request.session['errormsg']

            regi = Registration(
              regi_name = rname,
              regi_email = remail,
              regi_psw = rpsw
            )

            regi.save()

    prods = Addtoproduct.objects.all().values()
    context = {
        'products': prods,
    }
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

    


def gallery(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({},request))

def login(request):
    if request.method == 'POST':
        lname = request.POST["log_name"]
        lpsw = request.POST["log_psw"]
        
        log = Registration.objects.filter(regi_name = lname , regi_psw = lpsw)
        if log:
            request.session['usersession'] = lname
            cart = Cart.objects.filter(cart_user = request.session['usersession'])
            cart_count = 0
            for x in cart:
                cart_count += x.cart_qty
                request.session['cart_count'] = cart_count
            return HttpResponseRedirect("/account")
        
    
    template = loader.get_template("login.html")
    return HttpResponse(template.render({},request))


def addtocart(request,id):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    
    exist = Cart.objects.filter(cart_proid=id,cart_user = request.session["usersession"])
    if exist:
        exstcart = Cart.objects.filter(cart_proid=id,cart_user = request.session["usersession"])[0]
        exstcart.cart_qty+=1
        exstcart.cart_amount = exstcart.cart_qty * exstcart.cart_price
        exstcart.save()
    else:
        pro = Addtoproduct.objects.filter(id=id)[0]

        cart = Cart(cart_user = request.session["usersession"],
                    cart_proid = pro.id,
                    cart_name = pro.pro_name,
                    cart_price = pro.pro_price,
                    cart_image = pro.pro_image,
                    cart_qty=1,
                    cart_amount = pro.pro_price )
        cart.save()
    cart = Cart.objects.filter(cart_user = request.session['usersession'])
    cart_count = 0
    for x in cart:
        cart_count += x.cart_qty
        request.session['cart_count'] = cart_count
    return HttpResponseRedirect("/cart")




def addtoproduct(request):
    if request.method =='POST':
        pro_name = request.POST['pro_name']
        pro_price = request.POST['pro_price']
        pro_image = request.FILES['pro_image']
        pro_desc = request.POST['pro_desc']

        product = Addtoproduct(
            pro_name = pro_name,
            pro_price = pro_price,
            pro_desc = pro_desc,
            pro_image = pro_image
        )
        product.save()

    template = loader.get_template("addtoproduct.html")
    return HttpResponse(template.render({},request))



def cart(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect("/login")
    
    #delete cart item 
    if 'del' in request.GET:
        id = request.GET['del']
        delcart = Cart.objects.filter(id=id)[0]
        delcart.delete()
        cart = Cart.objects.filter(cart_user = request.session['usersession'])
        cart_count = 0
        for x in cart:
            cart_count += x.cart_qty
            request.session['cart_count'] = cart_count
        
        #change cart quantity

    if 'q' in request.GET:
            q = request.GET['q']
            cp = request.GET['cp']
            cart2=Cart.objects.filter(id=cp)[0]

            if q =='inc':
                cart2.cart_qty+=1
            elif q =='dec':
                if(cart2.cart_qty>1):
                    cart2.cart_qty-=1
            cart2.cart_amount = cart2.cart_qty * cart2.cart_price
            cart2.save()
            cart = Cart.objects.filter(cart_user = request.session['usersession'])
            cart_count = 0
            for x in cart:
                cart_count += x.cart_qty
                request.session['cart_count'] = cart_count




                
        
    

    user = request.session["usersession"]
    cart2 = Cart.objects.filter(cart_user=user).values()
    cart2= Cart.objects.filter(cart_user=user)
    
    tot = 0
    for x in cart2:
        tot+=x.cart_amount

    shp = tot * 10/100
    gst = tot * 18/100

    gtot = tot+shp+gst

    request.session["tot"] = tot
    request.session["gst"] = gst
    request.session["shp"] = shp
    request.session["gtot"] = gtot

    context={
            'cart':cart2,
            'tot':tot,
            'shp':shp,
            'gst':gst,
            'gtot':gtot,



        }

            

    template = loader.get_template("cart.html")
    return HttpResponse(template.render(context,request))


def checkout(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect("/login")
    
    co = 0
    adrs = ptype = ""
    checkemail = checkout_email = ""
    checkphone = checkout_phone = ""
    checkname = checkout_name = ""
    checkcity = checkout_city = ""
    checkaddress = checkoutaddress = ""
    checkcountry = checkout_country = ""
    checkpostal = checkout_postal = ""

    if 'checkout_email' in request.POST:
        # ptype = request.POST["pay_type"]
        checkemail = request.POST["checkout_email"]
        checkphone = request.POST["checkout_phone"]
        checkname = request.POST["checkout_name"]
        checkaddress = request.POST["checkout_address"]
        checkcity = request.POST["checkout_city"]
        checkcountry = request.POST["checkout_country"]
        checkpostal = request.POST["checkout_postal"]
        co=1


    
    user = request.session["usersession"]

    old_odr = Order.objects.filter(order_user=user,order_status=0)
    old_odr.delete()

    cart=Cart.objects.filter(cart_user=user)
    for x in cart:
        odr = Order(
            order_user = x.cart_user,
            order_name = x.cart_name,
            order_price = x.cart_price,
            order_image = x.cart_image,
            order_qty = x.cart_qty,
            order_amount = x.cart_amount,
            order_address = adrs,
            order_paytype = ptype,
            order_status = 0,
            checkout_email = checkemail,
            checkout_phone = checkphone,
            checkout_name = checkname,
            checkout_address = checkaddress,
            checkout_city = checkcity,
            checkout_country = checkcountry,
            checkout_postal = checkpostal
        )
        odr.save()

    order = Order.objects.filter(order_user=user,order_status=0).values()

    tot = request.session["tot"]
    gst = request.session["gst"]
    shp = request.session["shp"]
    gtot = request.session["gtot"]

    if co==1:
        return HttpResponseRedirect("/confirmorder")

    context = {
        'order':order,
        'tot':tot,
        'gst':gst,
        'shp':shp,
        'gtot':gtot,
        'co':co
    }
            
    template = loader.get_template("checkout.html")
    return HttpResponse(template.render(context,request))

def confirmorder(request):
       
    if'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    
    co = 0
    adrs = ptype = ""
    checkemail = checkout_email = ""
    checkphone = checkout_phone = ""
    checkname = checkout_name = ""
    checkcity = checkout_city = ""
    checkaddress = checkoutaddress = ""
    checkcountry = checkout_country = ""
    checkpostal = checkout_postal = ""


    if 'checkout_email' in request.POST:
        # ptype = request.POST["pay_type"]
        checkemail = request.POST["checkout_email"]
        checkphone = request.POST["checkout_phone"]
        checkname = request.POST["checkout_name"]
        checkaddress = request.POST["checkout_address"]
        checkcity = request.POST["checkout_city"]
        checkcountry = request.POST["checkout_country"]
        checkpostal = request.POST["checkout_postal"]
        co=1


    user = request.session["usersession"]

    old_odr = Order.objects.filter(order_user=user,order_status=0)
    old_odr.delete()


    cart=Cart.objects.filter(cart_user=user)
    for x in cart:
        odr = Order(
            order_user = x.cart_user,
            order_name = x.cart_name,
            order_price = x.cart_price,
            order_image = x.cart_image,
            order_qty = x.cart_qty,
            order_amount = x.cart_amount,
            order_address = adrs,
            order_paytype = ptype,
            order_status = 0,
            checkout_email = checkemail,
            checkout_phone = checkphone,
            checkout_name = checkname,
            checkout_address = checkaddress,
            checkout_city = checkcity,
            checkout_country = checkcountry,
            checkout_postal = checkpostal
        )
        odr.save()

    order = Order.objects.filter(order_user=user,order_status=0).values()
    
    user = request.session["usersession"]
    order = Order.objects.filter(order_user=user,order_status=0)
    for x in order:
        x.order_status=1
        x.save()

    template = loader.get_template("confirmorder.html")
    return HttpResponse(template.render({}, request))

def myorders(request):
    user = request.session["usersession"]
    order = Order.objects.filter(order_user=user,order_status=1)
   
        # Check if the 'del' parameter is in the GET request
    if 'del' in request.GET:
        id = request.GET['del']
        # Use get_object_or_404 to safely retrieve the order
        delcart = Order.objects.filter(id=id)[0] 
        delcart.delete()
        # Redirect to the orders page with a success message (optional)

    order = Order.objects.filter(order_user=user)


    context = {
        'order':order
    }


  
    template = loader.get_template("myorders.html")
    return HttpResponse(template.render(context,request))




def account(request):
    if'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    if 'del' in request.GET: 
        reg_id=request.GET['del']
        profile = Registration.objects.filter(id = reg_id).first()
        profile.regi_img = None
        profile.save()
        return HttpResponseRedirect('/account')

    if request.method == 'POST' and request.FILES.get('acc_img'):
        profile = Registration.objects.filter(regi_name = request.session['usersession']).first()
        profile.regi_img = request.FILES['acc_img']
        profile.save()
        return HttpResponseRedirect('/account')
    if 'acc_email' in request.POST:
        email = request.POST['acc_email']
        psw = request.POST['acc_psw']
        profile = Registration.objects.filter(regi_name = request.session['usersession']).first()
        profile.regi_email = email
        profile.regi_psw = psw
        profile.save()
        return HttpResponseRedirect('/account')


    register=Registration.objects.filter(regi_name=request.session['usersession']).first()
    
    context = {
        'register':register
     }
    template = loader.get_template("account.html")
    return HttpResponse(template.render(context,request))





def logout(request):
    if 'usersession' in request.session:
        del request.session['usersession']
        return HttpResponseRedirect('/')
    
