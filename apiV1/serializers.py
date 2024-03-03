from rest_framework import serializers

from .models import Product, Student, Lesson


class StudentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = Student.objects.create(**validated_data)
        return user

    class Meta:
        model = Student
        fields = ('id', 'name', 'age', 'gender', 'email')


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Product
        fields = ['id', 'name', 'start_date', 'cost', 'lessons_count']


class ProductInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    students_count = serializers.IntegerField()
    groups_fill_percentage = serializers.FloatField()
    product_purchase_percentage = serializers.FloatField()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'product', 'title', 'video_link']
