# Generated by Django 4.2.5 on 2023-09-20 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_remove_product_access_productaccess_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='products',
        ),
        migrations.AddField(
            model_name='product',
            name='lessons',
            field=models.ManyToManyField(to='application.lesson'),
        ),
    ]
