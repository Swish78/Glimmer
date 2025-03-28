# Generated by Django 4.2.3 on 2025-02-16 18:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_review_rating"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="review",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="review",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image1",
            field=models.ImageField(upload_to="product_images/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="image2",
            field=models.ImageField(blank=True, null=True, upload_to="product_images/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="image3",
            field=models.ImageField(blank=True, null=True, upload_to="product_images/"),
        ),
    ]
