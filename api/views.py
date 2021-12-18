from datetime import datetime
from django.contrib.auth import login, logout, tokens
from django.contrib.auth.models import User
from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .resetform import resetforms
from api.insertform import ProductForm
from .serializers import CartSerializer,CategorySerializer, OrderSreializer, ProductSerializer, TestSerializer, UserSerializer
from product.models import Category, Product, imgSrc, testclass
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,force_text,DjangoUnicodeDecodeError
from .utils import generate_token,reset_token
from django.core.mail import EmailMessage
from django.core import mail
from dbproject.settings import EMAIL_HOST_USER
from User.models import Profile
from cart.models import CartProduct,Cart
from orders.models import OrderProduct,Order
# from django.contrib.auth.models import User as authuser
import threading
from django.db import connection, connections
class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)

    def run(self):
        mail.send_mail(self.email["subject"],self.email["body"],EMAIL_HOST_USER,self.email["to"],html_message=self.email["body"])

@api_view(['GET'])
def categories(request):
    category=Category.objects.raw('SELECT * FROM PRODUCT_CATEGORY')
    categories=[]
    for cat in category:
        categories.append(cat)
    # print(connection.queries)
    serializer=CategorySerializer(categories,many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def test(request):
#     obj=testclass.objects.all()
#     ser=TestSerializer(obj,many=True)
#     return Response(ser.data)

@api_view(['GET'])
def Catwiseproducts(request,pk):
    print(pk)
    category=Category.objects.raw("SELECT * FROM PRODUCT_CATEGORY WHERE PRODUCT_CATEGORY.ID = %s",[pk])
    product=Product.objects.raw("SELECT * FROM PRODUCT_PRODUCT WHERE PRODUCT_PRODUCT.categoryId_id = %s",[category[0].id])
    print(product[0])
    products=[]
    for prod in product:
        products.append(prod)
    ser=ProductSerializer(products,many=True)
    return Response(ser.data)

@api_view(['GET'])
def product(request,pk):
    product=Product.objects.raw("SELECT * FROM PRODUCT_PRODUCT WHERE PRODUCT_PRODUCT.ID = %s",[pk])

    ser=ProductSerializer(product[0],many=False)
    return Response(ser.data)

@api_view(['GET'])
def allproducts(request):
    # products=Product.objects.all()
    product=Product.objects.raw('SELECT * FROM PRODUCT_PRODUCT')
    products=[]
    for prod in product:
        print(prod)
        products.append(prod)
    ser=ProductSerializer(products,many=True)
    return Response(ser.data)

@api_view(['POST'])
def createuser(request):
    data=request.data
    try:
        user=User.objects.raw('SELECT * FROM AUTH_USER WHERE EMAIL=%s',[request.data['email']])
        user=user[0]
        # print(user.username)
        data={'ERROR':'USER WITH THIS EMAIL ALREADY EXISTS'}
        print(data)
        return Response(data)
    except:
        #    user=User.objects.create(
        #     username=data["username"],
        #     password=make_password(data["password"]),
        #     email=data["email"],
        # )
        cursor=connection.cursor()
        cursor.execute('INSERT INTO AUTH_USER (USERNAME,PASSWORD,EMAIL,IS_SUPERUSER,last_name,is_active,date_joined,first_name,is_staff) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',[data['username'],make_password(data['password']),data['email'],False,'',True,datetime.now(),'',False])
        user=User.objects.latest('id')
        # print('ss')
        cursor.execute('insert into user_profile (user_id,phoneno,city,is_verified) values(%s,%s,%s,%s)',[user.id,request.data['phone'],request.data['city'],False])
        # profile=Profile.objects.raw('SELECT * FROM USER_PROFILE WHERE USER_ID=%s',[user.id])
        # cursor=connection.cursor()
        # cursor.execute('update user_profile set phoneno=%s, city=%s where user_id=%s',[request.data['phone'],request.data['city'],user.id])
        # user.save()
        return Response("USER CREATED")

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def sendverificationemail(request):
    # user=request.user
    user=User.objects.raw('SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."id" = %s',[request.user.id])
    user=user[0]
    profile=Profile.objects.get(user=user)
    print(connection.queries)
    current_site=get_current_site(request)
    email_subject="Activate Your Account \U0001f600"
    email_body=render_to_string('api/activate.html',{
        'user':user,
    'domain':current_site,
    'uid':urlsafe_base64_encode(force_bytes(user.id)),
    'token': generate_token.make_token(user)
    })
    email={"subject":email_subject,"body":email_body,"from_email":EMAIL_HOST_USER,"to":[user.email]}
    # mail.send_mail(email_subject,email_body,EMAIL_HOST_USER,[user.email],html_message=email_body)
    EmailThread(email).start()
    print("\U0001f600")
    return Response("USER")



def activate_user(request,uid64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uid64))
        user=User.objects.raw('SELECT * FROM "auth_user" WHERE "auth_user"."id" = %s',[uid])
        print(user[0].username)
        user=user[0]
    except Exception as e:
        user=None

    if user and generate_token.check_token(user,token):
        profile=Profile.objects.raw('SELECT * FROM "User_profile" WHERE "User_profile"."user_id" = %s',[user.id])
        profile=profile[0]
        profile.is_verified=True
        profile.save()
        print("EMAIL VERIFIED")
        return HttpResponse("VERIFIED")
    return HttpResponse("NOT VERIFIED")

@api_view(['POST','GET'])
def resetPassword(request):
    email=request.data['email']
    current_site=get_current_site(request)
    try:
        # user=User.objects.get(email=email)
        user=User.objects.raw('SELECT * FROM "auth_user" WHERE "auth_user"."email" = %s',[email])
        user=user[0]
    except:
        user=None
    if user is not None:
        email_subject="Password Reset \U0001f600"
        email_body=render_to_string("api/reset.html",{
            "user":user,
            "domain":current_site,
            "token":reset_token.make_token(user),
            "uid":urlsafe_base64_encode(force_bytes(user.id))
        })
        email={"subject":email_subject,"body":email_body,"from_email":EMAIL_HOST_USER,"to":[user.email]}
        EmailThread(email).start()
        return JsonResponse("Password Reset email sent",safe=False)

    return JsonResponse("No email found",safe=False)

def renderreset(request,uid64,token):
    form=resetforms()
    return render(request,'api/passwordresetform.html',{"uid":uid64,"token":token,"form":form})

@api_view(['POST','GET'])
def resetPasswordStep2(request,uid64,token):
        
        uid=force_text(urlsafe_base64_decode(uid64))
        
        # user=User.objects.get(id=uid)
        user=User.objects.raw('SELECT * FROM "auth_user" WHERE "auth_user"."id" = %s',[uid])
        user=user[0]
        print(request.POST)
        print(user.password)
        if reset_token.check_token(user,token):
            data=request.POST
            user.password=make_password(data['password'])
            user.save()
            login(request,user)
            logout(request)
            return JsonResponse("PASSWORD CHANGED",safe=False)
        return JsonResponse("Link expired or TOken already used !",safe=False)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def addtoCart(request):
    id=request.data['id']
    user=request.user
    profile=Profile.objects.raw('SELECT * FROM "User_profile" WHERE "User_profile"."user_id" = %s',[user.id] )
    profile=profile[0]
    # cart,created=Cart.objects.get_or_create(
    #     profile=profile
    # )
    # print(type(profile.id))
    try:
        cart=Cart.objects.raw('SELECT * FROM CART_CART WHERE CART_CART.PROFILE_ID= %s',[profile.id])
        cart=cart[0]
    except:
        # cart=Cart.objects.create(profile=profile)
        cursor=connections['default'].cursor()
        cursor.execute("INSERT INTO CART_CART (PROFILE_ID,PRICE) VALUES(%s,%s)",[profile.id,0])
        cart=Cart.objects.raw('SELECT * FROM CART_CART WHERE CART_CART.PROFILE_ID= %s',[profile.id])
        cart=cart[0]

    # print(connection.queries)
    # product=Product.objects.get(id=id)
    # print(connection.queries)
    product=Product.objects.raw('select * from product_product where product_product.id=%s',[id])
    product=product[0]
   

    # cartproduct,created=CartProduct.objects.get_or_create(product=product,profile=profile,cart=cart)
    # if not created:
    #     cartproduct.quantity=cartproduct.quantity+1
    #     cartproduct.save()
    if product.in_stock>0:
        try:
            cartproduct=CartProduct.objects.raw('SELECT * FROM CART_CARTPRODUCT WHERE CART_CARTPRODUCT.PRODUCT_ID= %s AND CART_CARTPRODUCT.CART_ID= %s',[product.id,cart.id])
            # print(cartproduct[0])
            cartproduct=cartproduct[0]
            # print(cartproduct.quantity)
            cartproduct.quantity=cartproduct.quantity+1
            cartproduct.save()
        except:
            cursor=connections['default'].cursor()
            cursor.execute('INSERT INTO CART_CARTPRODUCT (id,PRODUCT_ID,CART_ID,quantity) VALUES(%s,%s,%s,%s)',[89,product.id,cart.id,1])
            cartproduct=CartProduct.objects.raw('SELECT * FROM CART_CARTPRODUCT WHERE CART_CARTPRODUCT.PRODUCT_ID= %s AND CART_CARTPRODUCT.CART_ID= %s',[product.id,cart.id])
            # print(cartproduct[0])
            cartproduct=cartproduct[0]
        product.in_stock=product.in_stock-1
        product.save()
        # if product.in_stock<0:
        #     product.instock=0
        product.save()
        cart.price=cart.price+(cartproduct.product.price)
        cart.save()
        ser=CartSerializer(cart,many=False)
        return Response(ser.data)
    return Response('OutofStock')

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def removefromcart(request):
    user=request.user
    profile=Profile.objects.raw('SELECT * FROM USER_PROFILE WHERE USER_ID = %s',[user.id])
    profile=profile[0]
    cart=Cart.objects.raw('SELECT * FROM CART_CART WHERE CART_CART.PROFILE_ID=%s',[profile.id])
    cart=cart[0]
    id=request.data['id']
    cartproduct=CartProduct.objects.raw('SELECT * FROM CART_CARTPRODUCT WHERE CART_CARTPRODUCT.ID=%s',[id])
    cartproduct=cartproduct[0]
    cartproduct.product.in_stock=cartproduct.product.in_stock+1
    cartproduct.product.save()
    cartproduct.quantity=cartproduct.quantity-1
    if cartproduct.quantity<=0:
        cursor=connection.cursor()
        cursor.execute('DELETE FROM CART_CARTPRODUCT WHERE CART_CARTPRODUCT.ID=%s',[cartproduct.id])
        cart.price=cart.price-(cartproduct.product.price)
        # cursor.execute('UPDATE CART_CART SET CART_CART.PRICE=%s [where CART_CART.PROFILE_ID]=%s',[a,profile.id])
        print(connection.queries)
        cart.save()
    else:
        cartproduct.save()
        cart.price=cart.price-(cartproduct.product.price)
        cart.save()
    
    
        # cartproduct.price=cartproduct.price-(cartproduct.product.price)
    return Response('Item quantity removed by 1')

@api_view(['POST'])
@permission_classes([IsAdminUser])
def insertproduct(request):
    print(request.data)
    name=request.data['name']
    category=request.data['category']
    cat=Category.objects.get(id=category)
    price=request.data['price']
    primary_image=request.data['primary_image']
    description=request.data['description']
    in_stock=request.data['in_stock']
    cursor=connections['default'].cursor()
    # cursor.execute('INSERT INTO PRODUCT_PRODUCT (NAME,CATEGORYID_ID,PRICE,PRIMARY_IMAGE,DESCRIPTION,IN_STOCK) VALUES(%s,%s,%s,%s,%s,%s)',[name,category,price,primary_image,description,in_stock])
    product=Product.objects.create(name=name,categoryId=cat,price=price,primary_image=primary_image,description=description,in_stock=in_stock)
    try:
        img1=imgSrc.objects.create(url=request.data['img1'],product=product)
        img2=imgSrc.objects.create(url=request.data['img2'],product=product)
        img3=imgSrc.objects.create(url=request.data['img3'],product=product)
    except:
       pass 
    data={'status':'INSERTED'}
    return Response(data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteproduct(request):
    id=request.data['id']
    cursor=connections['default'].cursor()
    cursor.execute('DELETE FROM PRODUCT_PRODUCT WHERE ID=%s',[id])
    data={'status':'DELETED'}
    return Response(data)



@api_view(['POST'])
@permission_classes([IsAdminUser])
def updateproduct(request):
    print(request.data)
    product=Product.objects.raw('SELECT * FROM PRODUCT_PRODUCT WHERE ID=%s',[request.data['id']])
    product=product[0]
    product.name=request.data['name']
    cat=Category.objects.raw('SELECT * FROM PRODUCT_CATEGORY WHERE ID=%s',[request.data['category']])
    product.categoryId=cat[0]
    product.price=request.data['price']
    product.primary_image=request.data['primary_image']
    product.description=request.data['description']
    product.in_stock=request.data['in_stock']
    product.save()

    try:
        images=imgSrc.objects.raw('SELECT * FROM product_imgSrc where product_id=%s',[product.id])
        images[0].url=request.data['img1']
        images[1].url=request.data['img2']
        images[2].url=request.data['img3']
    except:
        pass
    # cursor=connection.cursor()
    # cursor.execute('UPDATE PRODUCT_PRODUCT SET PRICE=%s,PRIMARY_IMAGE=%s,CATEGORYID_ID=%s,DESCRIPTION=%s,IN_STOCK=%s,NAME=%s WHERE ID=%s',[request.data['price'],request.data['primary_image'],request.data['category'],request.data['description'],request.data['in_stock'],request.data['name'],request.data['id']])
    data={'status':'UPDATED'}
    return Response(data)

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def placeOrder(request):
    user=request.user
    c=request.data['cart'][0]
    # print(c['price'])
    cursor=connection.cursor()
    cursor.execute('INSERT INTO orders_Order (total_price,status,owner_id,created_at) VALUES (%s,%s,%s,%s)',[c['price'],'PENDING',c['profile'],datetime.now()])
    obj=Order.objects.latest('id')
    for ca in c['cartproduct']:
        cursor.execute('INSERT INTO ORDERS_ORDERPRODUCT (PRODUCT_ID,ORDER_ID,QUANTITY) VALUES (%s,%s,%s)',[ca['product']['id'],obj.id,ca['quantity']])
    ser=OrderSreializer(obj,many=False)
    print("A: ",c['id'])
    cart=Cart.objects.raw('SELECT * FROM CART_CART WHERE PROFILE_ID=%s',[user.profile.id])
    cart=cart[0]
    cart.delete()
    # cursor.execute('DELETE FROM CART_CART WHERE ID = %s',[cart.id])
    # data={'status':'Printed'}
    return Response(ser.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deletecart(request):
    user=request.user
    cart=Cart.objects.raw('SELECT * FROM CART_CART WHERE PROFILE_ID=%s',[user.profile.id])
    cart=cart[0]
    # cart.delete()
    cursor=connections['default'].cursor()
    print(cart.id)
    cursor.execute('DELETE FROM CART_CART WHERE ID=%s',[14])
    return Response('DELETED')



@api_view(['GET'])
@permission_classes([IsAdminUser])
def vieworder(request):
    orders=Order.objects.raw('SELECT * FROM ORDERS_ORDER ORDER BY created_at DESC')
    order=[]
    for o in orders:
        order.append(o)
    ser=OrderSreializer(order,many=True)
    return Response(ser.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateorderstatus(request):
    order=Order.objects.raw('SELECT * FROM ORDERS_ORDER WHERE ID=%s',[request.data['id']])
    order=order[0]
    cursor=connection.cursor()
    cursor.execute('UPDATE ORDERS_ORDER SET STATUS=%s where id=%s',[request.data['status'],order.id])
    data={"STATUS":"STATUS UPDATED"}
    return Response(data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getuserprofile(request):
    user=request.user
    ser=UserSerializer(user,many=False)
    return Response(ser.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def viewcart(request):
    user=request.user
    profile=Profile.objects.raw('SELECT * FROM USER_PROFILE WHERE USER_ID=%s',[user.id])
    profile=profile[0]
    cart=Cart.objects.raw('SELECT * from CART_CART where profile_id=%s',[profile.id])
    ser=CartSerializer(cart,many=True)
    return Response(ser.data)       

#REQUIRES A 'name' ONLY    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def insertcategory(request):
    cursor=connection.cursor()
    cursor.execute('INSERT INTO PRODUCT_CATEGORY (NAME,CREATED) VALUES(%s,%s)',[request.data['name'],datetime.now()])
    return Response('INSERTED')

#REQUIRES A 'id' ONLY
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deletecategory(request):
    cursor=connection.cursor()
    cursor.execute('DELETE FROM PRODUCT_CATEGORY WHERE ID=%s',[request.data['id']])
    return Response('DELETED')

#REQUIRES BOTH 'name' AND 'id'
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updatecategory(request):
    cursor=connection.cursor()
    cursor.execute('UPDATE PRODUCT_CATEGORY SET NAME=%s where id=%s',[request.data['name'],request.data['id']])
    return Response('UPDATED')

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getallusers(request):
    # cursor=connection.cursor()
    user=User.objects.raw('SELECT * FROM AUTH_USER u JOIN USER_PROFILE p WHERE u.id=p.user_id')
    ser=UserSerializer(user,many=True)
    return Response(ser.data)

# @api_view(['POST'])
# def upload_img(request):
#     product=Product.objects.get(id=10)
#     product.primary_image=request.data['image']
#     product.save()
#     return Response('saass')

# def image(request,pk):
#     product=Product.objects.get(id=pk)
#     form=ProductForm(product)
#     return render(request,'api/product.html',{'form':form})