# Generated by Django 4.2 on 2025-01-02 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='chat_images/'),
        ),
    ]