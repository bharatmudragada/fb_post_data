# Generated by Django 2.2.1 on 2019-07-27 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_post', '0008_merge_20190727_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='name',
            field=models.CharField(default='', max_length=60),
            preserve_default=False,
        ),
    ]