# Generated by Django 4.1.5 on 2023-01-29 04:48

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='DefaultImages/user.jpg', upload_to=user.models.upload_location),
        ),
    ]
