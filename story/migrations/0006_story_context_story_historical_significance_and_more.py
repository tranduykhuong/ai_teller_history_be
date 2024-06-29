# Generated by Django 4.0.10 on 2024-06-29 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0005_story_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='context',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='story',
            name='historical_significance',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='story',
            name='main_happenings',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='story',
            name='result',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='storyimages',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
    ]
