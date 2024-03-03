from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from django.contrib.auth.models import User
from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404
from .dependences import (
    distribute_users_before_started,
    distribute_users_after_started,
    user_has_access_to_product)

from .serializers import StudentSerializer, LessonSerializer, ProductInfoSerializer
from .models import Product, Student, Lesson, Group, UserProductAccess
from datetime import datetime


# _________________________________________________________________________________________
# D I S T R I B U T E  => => P A R T
# Done
class DistributeUsersView(APIView):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if product.start_date > datetime.now():
            distribute_users_before_started(product)
        else:
            distribute_users_after_started(product)
        return Response({'message': 'Users distributed successfully.'})
# D I S T R I B U T E  => => P A R T
# _________________________________________________________________________________________


# _________________________________________________________________________________________
# S T U D E N T  => => P A R T
# Done
class StudentListAPIView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_object(self, pk):
        student = get_object_or_404(Product, id=pk)
        return student

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            student = self.get_object(kwargs['pk'])
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        else:
            students = self.get_queryset()
            serializer = self.get_serializer(students, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# S T U D E N T  => => P A R T
# _________________________________________________________________________________________


# _________________________________________________________________________________________
# P R O D U C T  => => P A R T
class ProductLessonsAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        if user_has_access_to_product(product_id, self.request.user):
            return Lesson.objects.filter(product_id=product_id)
        return Lesson.objects.none()


class ProductInfoAPIView(ListAPIView):
    serializer_class = ProductInfoSerializer

    def get_queryset(self):
        products = Product.objects.all()
        products_info = []
        for product in products:
            students_count = UserProductAccess.objects.filter(
                product=product).count()

            max_group_size = product.max_group_size
            filled_groups_avg = Group.objects.filter(product=product).annotate(
                participants_count=Count('students')
            ).aggregate(avg_filled_groups=Avg('participants_count'))['avg_filled_groups'] or 0
            groups_fill_percentage = (
                filled_groups_avg / max_group_size) * 100 if max_group_size != 0 else 0

            total_users_count = User.objects.count()
            product_access_count = UserProductAccess.objects.filter(
                product=product).count()
            product_purchase_percentage = (
                product_access_count / total_users_count) * 100 if total_users_count != 0 else 0

            products_info.append({
                'name': product.name,
                'students_count': students_count,
                'groups_fill_percentage': groups_fill_percentage,
                'product_purchase_percentage': product_purchase_percentage
            })

        # Возвращаем список информации о продуктах
        return products_info

# P R O D U C T  => => P A R T
# _________________________________________________________________________________________
