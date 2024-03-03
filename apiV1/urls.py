from django.contrib import admin
from django.urls import path
from .views import StudentListAPIView, DistributeUsersView, ProductInfoAPIView, ProductLessonsAPIView


urlpatterns = [
    path('students/', StudentListAPIView.as_view(), name='students'),
    path('distribute/', DistributeUsersView.as_view(), name='distribute'),
    path('products/', ProductInfoAPIView.as_view(), name='products'),
    path('products/<int:product_id>/lessons/',
         ProductLessonsAPIView.as_view(), name='product-lessons-list'),
]
