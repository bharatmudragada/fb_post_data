# Generated by Django 2.2.1 on 2019-07-26 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='postBody',
            new_name='post_body',
        ),
    ]