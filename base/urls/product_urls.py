from django.urls import path
from base.views import product_views as views



urlpatterns = [
    
    path('',views.getProducts,name='products'),
    
    path('top/',views.getTopProducts, name='top-products'),
    path('store/',views.getStoreProducts, name='store-products'),
    path('category/',views.getCategory,name='product-category'),
    path('category/create/',views.createCategory,name='category-create'),
    path('filter/',views.getFilterProducts,name='product-filter'),
    path('create/',views.createProduct,name='product-create'),
    path('upload/',views.uploadImage,name='image-upload'),
    

    
    path('<str:pk>/',views.getProduct,name='product'),
    
    
    
    path('category/<str:pk>/',views.getCategoryDetails,name='category-details'),
    
    
    path('update/<str:pk>/',views.updateProduct,name='product-update'),
    path('delete/<str:pk>/',views.deleteProduct,name='product-delete'),
    
    
    
    path('category/delete/<str:pk>/',views.deleteCategoryt,name='category-delete'),
    path('category/update/<str:pk>/',views.updateCategory,name='category-update'),
    
    
    path('<str:pk>/reviews/',views.createProductReview,name='create-review'),

    
]
