from rest_framework import serializers

from .models import Product, Lesson, LessonView


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['view_time', 'viewed', 'last_time_viewed']


class LessonSerializer(serializers.ModelSerializer):
    lessonview_set = LessonViewSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'duration', 'video_url', 'lessonview_set']


class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'lessons']


class ProductStatsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(source='id')
    product_name = serializers.CharField(source='name')
    total_lesson_views = serializers.IntegerField()
    total_view_time = serializers.IntegerField()
    total_students = serializers.IntegerField()
    purchase_percentage = serializers.FloatField()
