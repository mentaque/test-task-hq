from django.contrib.auth.models import User
from django.db.models import Count, Sum, Prefetch
from django.db.models.functions import Round
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, LessonView
from .serializers import ProductSerializer, ProductStatsSerializer


class LessonListView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('user', openapi.IN_QUERY, description="user id", type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter('product', openapi.IN_QUERY, description="product id", type=openapi.TYPE_INTEGER),
    ])
    def get(self, request):
        user_id = self.request.query_params.get('user')
        product_id = self.request.query_params.get('product')
        if product_id:
            products = Product.objects.filter(
                id=product_id
            ).filter(
                productaccess__user_id=user_id
            ).prefetch_related(Prefetch(
                'lessons__lessonview_set',
                queryset=LessonView.objects.filter(user_id=user_id)
            ))
        else:
            products = Product.objects.filter(
                productaccess__user_id=user_id
            ).prefetch_related(Prefetch(
                'lessons__lessonview_set',
                queryset=LessonView.objects.filter(user_id=user_id)
            ))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductStatsView(APIView):
    def get(self, request):
        total_users = User.objects.count()
        products_stats = Product.objects.annotate(
            total_lesson_views=Count('lessons__lessonview', distinct=True),
            total_view_time=Sum('lessons__lessonview__view_time'),
            total_students=Count('productaccess', distinct=True),
            purchase_percentage=Round((Count('productaccess', distinct=True) / float(total_users)) * 100, 2)
        ).values(
            'id', 'name', 'total_lesson_views', 'total_view_time', 'total_students', 'purchase_percentage'
        )

        serializer = ProductStatsSerializer(products_stats, many=True)
        return Response(serializer.data)



