# Generated by Django 4.0.10 on 2024-06-29 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0004_alter_storyimages_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='summary',
            field=models.CharField(default=None, max_length=500),
            preserve_default=False,
        ),
    ]
