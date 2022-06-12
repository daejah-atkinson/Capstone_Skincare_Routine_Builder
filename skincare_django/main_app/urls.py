from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('routines/', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"), 
    path('favorites/', views.FavoriteProduct.as_view(), name="favorites"), 
    path('products/', views.ProductList.as_view(), name="product_list"), 
    path('products/<int:pk>/', views.ProductDetail.as_view(), name="product_detail"), 
    path('products/<int:pk>/brands/new', views.BrandCreate.as_view(), name="brand_create"),
    path('routines/<int:pk>/brands/<int:brand_pk>/', views.RoutineBrandAssoc.as_view(), name="routine_brand_assoc"), 
    path('products/<int:pk>/brands/', views.BrandDetail.as_view(), name="brand_detail"), 
    path('brands/<int:pk>/update',views.BrandUpdate.as_view(), name="brand_update"),
    path('favorites/<int:pk>/brands/<int:brand_pk>/', views.FavoriteBrandAssoc.as_view(), name="favorite_brand_assoc"), 
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
    path('', RedirectView.as_view(pattern_name='product_list', permanent=False)),
    
]

