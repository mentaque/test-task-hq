from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    lessons = models.ManyToManyField('Lesson')

    def __str__(self):
        return self.name


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} for {self.product.name}'


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.IntegerField()

    def __str__(self):
        return self.title


class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    view_time = models.IntegerField()
    viewed = models.BooleanField(default=False)
    last_time_viewed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User: {self.user.username} - Lesson: {self.lesson}, viewed: {self.viewed}'

    def save(self, *args, **kwargs):
        if self.view_time > self.lesson.duration:
            raise ValidationError("Время просмотра не может быть больше длительности видео")

        view_percentage = (self.view_time / self.lesson.duration)

        if view_percentage >= 0.8:
            self.viewed = True

        super(LessonView, self).save(*args, **kwargs)

