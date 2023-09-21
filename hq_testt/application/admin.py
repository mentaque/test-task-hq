from django.contrib import admin

from application.models import LessonView, Lesson, ProductAccess, Product

admin.site.register(Product)
admin.site.register(ProductAccess)
admin.site.register(Lesson)
admin.site.register(LessonView)
