from django.urls import path
from . import views

urlpatterns = [
    path('',views.categories,name='category'),#send marshallized categories data
    # path('test',views.test),
    path('categories/<str:pk>/products',views.Catwiseproducts,name="products"),#send products wrt categoires
    path('product/<str:pk>',views.product,name="single"),#send single product
    path('products',views.allproducts,name="allproducts"),
    path('createuser',views.createuser,name='createuser'),
    path('sendemaill',views.sendverificationemail,name='sendmail'),
    path('activate/<uid64>/<token>',views.activate_user,name='activate'),
    path('reset/<uid64>/<token>',views.renderreset,name='reset'),
    path('resetpassword',views.resetPassword,name='resetpassword'),
    path('resetpassword2/<uid64>/<token>',views.resetPasswordStep2,name='resetpassword2'),
    path('addtocart',views.addtoCart,name="addtocart"),
    path('removefromcart',views.removefromcart,name='removecartproduct'),
    path('insertproduct',views.insertproduct,name='insertproduct'),
    path('deleteproduct',views.deleteproduct,name='deleteproduct'),
    path('updateproduct',views.updateproduct,name='updateproduct'),
    path('placeorder',views.placeOrder,name='PlaceOrder'),
    path('vieworder',views.vieworder,name='ViewOrder'),
    path('updateorderstatus',views.updateorderstatus,name='updateorderstatus'),
    path('getuser',views.getuserprofile,name='GetUserProfile'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('getallusers',views.getallusers,name='getallusers'),
    path('insertcategory',views.insertcategory,name='insertcategory'),
    path('deletecategory',views.deletecategory,name='deletecategory'),
    path('updatecategory',views.updatecategory,name='updatecategory'),
    path('deletecart',views.deletecart,name='deletecart'),
    # path('uploadimg',views.upload_img,name='uploadimage'),
    # path('image/<str:pk>',views.image,name='image')
    ]